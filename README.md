# ANova Finance Reimbursement Script
This tool automates submitting purchase requests on Callink using [Selenium](https://www.selenium.dev). Using the Reimbursement Submission Form response spreadsheet, it retrieves ALL Stage 0 purchase requests and puts them all in Stage 1 on Callink.

**You must be a Stage 2 Financial Requester/Agent for the club in order to use this script.**

## Prerequisites

### Install Dependencies
1. Run `pip install -r requirements.txt` to install all necessary dependencies.


### Enable the Google Sheets API
1. Go to [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python?authuser=1#step_1_turn_on_the) and complete Step 1.
2. If asked to configure your OAuth client, select `Desktop App`.
3. Click `DOWNLOAD CLIENT CONFIGURATION` and put the downloaded `credentials.json` into `/anova_finance`.

### Retrieve your Google Profile
The reimbursement script requires you to not have any other Chrome windows open, but for you to already be logged into your account to access the reimbursement spreadsheet.

1. Open Google Chrome and log in to your Berkeley email.
2. In a new tab, go to chrome://version and copy your Profile Path. On Mac, it should look something like `/Users/name/.../Google/Chrome/Default`.
3. In `submission.py`, paste your profile path as a string to `PROFILE_PATH`.

Now, each time you use the script to access Chrome, you login cookie will be stored in `CallinkCookie.pkl`.

## Running the Reimbursement Script
Currently, the script submits all purchase requests that have not been submitted yet (in Stage 0). This is based on the Reimbursement Submission Google Form responses. All purchase requests are in Stage 0 until it is submitted on Callink.

### Submitting all Stage 0 Reimbursements:
1. **MAKE SURE YOU ClOSE ANY OPEN CHROME WINDOWS OR THE SCRIPT WILL NOT WORK!**
2. On the command line, `cd` into the root directory of this project: `/anova_finance`.
3. Run `python submission.py`

Google Chrome should automatically open and visit ANova's finance page on Callink. **Do not click anything** — the script will automatically fill in the values of the required fields on the Purchase Request Form based on the responses of the Reimbursement Submission Form response spreadsheet and submit them one-by-one.
