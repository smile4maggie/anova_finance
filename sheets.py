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
RANGE = 'Form Responses 1!A2:P'

class Reimbursements:
    def __init__(self):
        self.creds = None
        self.sheet = None

    def build_spreadsheet(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        service = build('sheets', 'v4', credentials=self.creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        self.values = result.get('values', [])

    def get_spreadsheet(self):
        return self.values

    def get_incomplete(self):
        """Select all reimbursements that are in Stage 0."""
        if not self.values:
            print('There are no reimbursement requests in Stage 0.')
        else:
            incomplete = []
            for i in range(len(values)):
                row = values[i]
                pr_dict = {
                    'id' : i + 2,
                    'first_name' : row[0],
                    'last_name' : row[1],
                    'description' : row[2],
                    'amount' : row[3],
                    'type' : row[4],
                    'street' : row[5],
                    'city' : row[6],
                    'state' : row[7],
                    'zip' : row[8],
                    'university_id' : row[9],
                    'email' : row[10],
                    'phone' : row[11],
                    'expenditure' : row[12],
                    'stage' : row[15]
                }
                if pr_dict['first_name'] and pr_dict['type'] != 'Alcohol' and pr_dict['stage'] == '0':
                    incomplete.append(pr_dict)
            return incomplete

    def set_stage(pr_id, stage):
        """
        Sets the purchase request on row pr_id to the specified stage.
        """
        cell = 'Form Responses 1!P' + str(pr_id) + ':P' + str(pr_id) 
        stage = {'values':[[stage]]}
        self.sheet.values().update(spreadsheetId=SPREADSHEET_ID, 
                                    range=cell, 
                                    valueInputOption="USER_ENTERED", 
                                    body=stage).execute()