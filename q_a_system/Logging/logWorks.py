from q_a_system.global_pack import constant
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def getInputQ():
    # questions = constant.quesGSheet.col_values(1)[1:]

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    quesGSheet = client.open("Code Behaviours").worksheet('Code_InputQ')
    data = quesGSheet.get_all_records()

    questions = []
    expectedAnswer = []
    expectedResource = []
    expectedProperty = []

    for i in range(0, len(data), 1):
        questions.append(data[i].get('Question'))
        try:
            expectedResource.append(data[i].get('Expected Resource'))
            expectedProperty.append(data[i].get('Expected Property'))
            expectedAnswer.append(data[i].get('Expected Answer'))
        except:
            expectedResource.append(None)
            expectedProperty.append(None)
            expectedAnswer.append(None)
    return questions, expectedResource, expectedProperty, expectedAnswer


def saveOneLog(content):
    insertRow = content
    # constant.logsGSheet.insert_row(insertRow, 2)

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    logsGSheet = client.open("Code Behaviours").worksheet('Code_Logs')
    logsGSheet.insert_row(insertRow, 2)

