from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = '1X3ag0R7dfMGbgTZx3FE_-FzxoPCnz65CIJJiDIjxSoM'

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
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

logFile = open("log.txt","a+")
# Call the Sheets API

        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print('%s' % (row))
    # values[2] = "Bataindia"
sheet = service.spreadsheets()
# print(sheet)

def GetExcelValues(range,Id):
    result = sheet.values().get(spreadsheetId=Id,
                                range=range).execute()
    # print(result)
    values = result.get('values', [])
    # print(values)
    if not values:
        print('error : Excel No data found.')
        logFile.write('error : Excel No data found.')
        return 0
    else:
        logFile.write('success: Excel Readable found')
        print('success: Excel Readable found')
        return values
def updateNSE(name,Id):
    Ticker_Range = 'B4'
    values = GetExcelValues(Ticker_Range,Id)
    values[0][0] = name.upper()
    request = sheet.values().update(spreadsheetId=Id, range=Ticker_Range, valueInputOption="USER_ENTERED", body={"values" : values})
    response = request.execute()
    logFile.write(response)
    print(response)
    logFile.write(response)

def GetLinks(Id):
    Links_Range = "B8:B18"
    values = GetExcelValues(Links_Range,Id)
    return values
def UpdateLink(Id,values):
    Links_Range = "B8:B18"
    request = sheet.values().update(spreadsheetId=Id, range=Links_Range, valueInputOption="USER_ENTERED", body={"values" : values})
    try:
        response = request.execute()
    except Exception as e:
        print("error : something went wrong or " + str(e))
        logFile.write("\nerror : something went wrong or " + str(e))
def GetCF(Id):
    Links_Range = "k21:B21"
    values = GetExcelValues(Links_Range,Id)
    return values
def UpdateCF(Id,values):
    CF_Range = "k21:B21"
    request = sheet.values().update(spreadsheetId=Id, range=CF_Range, valueInputOption="USER_ENTERED", body={"values" : values})
    try:
        response = request.execute()
    except Exception as e:
        logFile.write("\nerror : something went wrong or " + str(e))
        print("error : something went wrong or " + str(e))
