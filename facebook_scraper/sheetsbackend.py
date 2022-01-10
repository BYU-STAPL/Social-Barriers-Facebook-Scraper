from .ibackend import IBackend
#from .userprofilesheet import UserProfileSheet
#from .frsheet import FRSheet

class SheetsBackend(IBackend):
    def __init__(self, keysName, spreadsheetId, sheets=[]):
        self.keys = keysName
        self.spreadsheetId = spreadsheetId
        self.sheets = sheets
    
    def store_data(self, user_dto):
        for sheet in self.sheets:
            sheet.store_data(user_dto)
    def add_sheet(self, sheet):
        self.sheets.append(sheet)
