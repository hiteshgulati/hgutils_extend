import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os



def get_sheet(file_name):
    scope = ['https://spreadsheets.google.com/feeds']
    json_file = "spreadsheet.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(file_name).sheet1
    return sheet
