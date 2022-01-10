from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .isheet import ISheet

class FRSheet(ISheet):
    def __init__(self, keysName, spreadsheetId):
        self.keys = keysName
        self.spreadsheetId = spreadsheetId

    def store_data(self, user_dto):
        # Credentials
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = self.keys
        creds = None
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        #Sheet Manipulation
        SPREADSHEET_ID = self.spreadsheetId

        service = build('sheets', 'v4', credentials=creds)

        column_names = [('Name', 'ProfilePhoto')]
        data = list(zip(user_dto.fr_name_list, user_dto.fr_photo_list))

        values = column_names + data

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range="FriendRequests!A1:B100",
            valueInputOption = "USER_ENTERED",
            body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

