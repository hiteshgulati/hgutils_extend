import gspread
from oauth2client.service_account import ServiceAccountCredentials



def get_sheet(file_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(file_name).sheet1
    return sheet
