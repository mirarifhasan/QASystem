from q_a_system.global_pack import constant
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def saveOneLog(content):
    insertRow = content
    # constant.logsGSheet.insert_row(insertRow, 2)

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    logsGSheet = client.open("Code Behaviours").worksheet('Code_Logs')
    logsGSheet.insert_row(insertRow, 2)

