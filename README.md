# ANova Finance Reimbursement Script 

## Prerequisites

### Packages
1. Install Selenium: `pip install selenium`
2. Install the Google Client Library: `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


### Enable the Google Sheets API
1. Login to Google using a non-Berkeley email.
2. Go to https://console.developers.google.com/apis/dashboard and click 'Select a project'. Create a new project called 'ANova Finance Reimbursements' with no parent organization.
3. Go to https://developers.google.com/sheets/api/quickstart/python?authuser=1#step_1_turn_on_the and click the 'Enable the Google Sheets API' button.
4. If asked to configure your OAuth client, select 'Desktop App'.
5. Click 'DOWNLOAD CLIENT CONFIGURATION'and put the downloaded `credentials.json` into `/anova_finance`.

