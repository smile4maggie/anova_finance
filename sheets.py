from __future__ import print_function
import pickle
import os.path
from secrets import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# Allows read/write access to the user's sheets and their properties.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
values = result.get('values', [])

def get_incomplete():
    """Select all reimbursements that are in Stage 0."""
    if not values:
        print('There are no reimbursement requests in Stage 0.')
    else:
        incomplete = []
        for i in range(len(values)):
            row = values[i]
            if row[14] == 'Yes' and row[4] != 'Venmo':
                pr_id = i + 2
                incomplete.append(pr_id + row)
        return incomplete

def set_stage(pr_id, stage):
    """
    Sets the purchase request on row pr_id to the specified stage.
    """
    cell = 'Form Responses 1!P' + str(pr_id) + ':P' + str(pr_id) 
    stage = {'values':[[stage]]}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, 
                          range=cell, 
                          valueInputOption="USER_ENTERED", 
                          body=stage).execute()