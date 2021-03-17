from __future__ import print_function
from os import name
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
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

service = build('drive', 'v3', credentials=creds)

sservice = build('sheets', 'v4', credentials=creds)
sheet = sservice.spreadsheets()
# def CopyFile(service,"Bata India Ltd"):

logFile = open("Id.txt","a+")


def CheckFileDir(FileName):
    # page_token = None
    results = service.files().list(q="mimeType = 'application/vnd.google-apps.spreadsheet'",spaces='drive',fields="nextPageToken, files(id, name)",pageSize=400).execute()
    items = results.get('files', [])

    # print(len(items))
    # for i in items:  
    if not items:
        logFile.write('\nNo files found.')
        print('No files found.')
        return None
    else:
        # print('Files:')
        for item in items:
            # print(item['name'])
            if(item['name'] == FileName):
                print(FileName + " is already there")
                logFile.write("\n"+FileName + " is already there")
                # print(item['name'])
                return item['id']


def CopyToFolder(folderId,name):
    # Find Bata File
    MasterFile = CheckFileDir("Link of Sheet")
    print(MasterFile)

    file_id = CheckFileDir(name) 
    # Find sector if not then create
    # sector = CreateFolder(folder)
    if file_id == None:    
        newfile = {'name': name,'parents' : [ folderId ]}
        file = service.files().copy(fileId=MasterFile, body=newfile).execute()
        print("Success copying file")
        logFile.write("\nSuccess copying file")
        return file.get('id')
    else:
        c = 1
        while(True):
            name = name+str(c)
            print("Trying this name : " +name)
            file_id = CheckFileDir(name) 
        # Find sector if not then create
        # sector = CreateFolder(folder)
            if file_id == None:    
                newfile = {'name': name,'parents' : [ folderId ]}
                file = service.files().copy(fileId=MasterFile, body=newfile).execute()
                print("Success copying file")
                logFile.write("\nSuccess copying file")
                return file.get('id')
            else:
                c+=1

def getData(folder_id):
    try: 
        print("Program seems working")
        results = service.files().list(q="'{}' in parents".format(folder_id),spaces='drive',fields="nextPageToken, files(id, name)",pageSize=400).execute()
        items = results.get('files', [])
        # print(items)
        for item in items:
            # print("Name: " + item['name'] + " Id: " +item['id'] )
            getExcelIds(item['id'])
    except Exception as e:
        print(e)

names = []
ids = []
def getExcelIds (folder_id):
    try:
        results = service.files().list(q="'{}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'".format(folder_id),spaces='drive',fields="nextPageToken, files(id, name)",pageSize=400).execute()
        items = results.get('files', [])
        # print(items)
        for item in items:
            # print("Name: " + item['name'] + " Id: " +item['id'] )
            names.append([item['name']])
            ids.append([item['id']])
    except Exception as e:
        print(e)

def GetExcelValues(range,Id):
    result = sheet.values().get(spreadsheetId=Id,
                                range=range).execute()
    # print(result)
    values = result.get('values', [])
    # print(values)
    if not values:
        print('error : Excel No data found.')
        logFile.write("\nerror : Excel No data found.")
        return 0
    else:
        logFile.write("\nsuccess: Excel Readable found")
        print('success: Excel Readable found')
        return values

def UpdateValues(Id,values,col):
    start = col+"2"
    num = len(names) + 2
    end = col+str(num)
    Links_Range = start+":"+end
    request = sheet.values().update(spreadsheetId=Id, range=Links_Range, valueInputOption="USER_ENTERED", body={"values" : values})
    print("Successfully wrote column " + col)
    logFile.write("Successfully wrote column " + col)
    try:
        response = request.execute()
    except Exception as e:
        print("error : something went wrong or " + str(e))
        logFile.write("\nerror : something went wrong or " + str(e))

# stocks_id = "1DQSTHR2-oCsmHLYZx7lPTcR6Mu7_r9Iv"
stocks_id = "1v_8D9Sdtw8B9OLAMdttPCMwQ0nYcTMiW"
# GetNames("1fy0BNWAU64n2pWOQPvoG-BXFI2RqH_2DuwjfjC8Xss0")
newFileId =  CopyToFolder(stocks_id,"FilesDetails")
print(newFileId)
getData(stocks_id)
UpdateValues(newFileId,names,"A")
UpdateValues(newFileId,ids,"B")
# print(len(ids))
# getExcelIds("Stocks")
logFile.close() 