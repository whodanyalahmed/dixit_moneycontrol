from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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


# def CopyFile(service,"Bata India Ltd"):

logFile = open("log.txt","a+")

def CreateFolder(folder,parent=None):
    # Call the Drive v3 API
    # CheckFileDir(folder)
    print("folder/File is not there creating one...")
    logFile.write("\nfolder/File is not there creating one...")
    body = {
    'name': folder,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent:
        body['parents'] = [parent]
    file = service.files().create(body=body,
                                        fields='id').execute()
    print('Folder ID: %s'% file.get('id'))
    logFile.write('Folder ID: %s'% file.get('id'))
    return file.get('id')
    # print(u'{0}'.format(item['name']))

def CheckFileDir(FileName):
    page_token = None
    results = service.files().list(q="mimeType = 'application/vnd.google-apps.spreadsheet'",spaces='drive',fields="nextPageToken, files(id, name)",pageToken=page_token).execute()
    items = results.get('files', [])

    # print(len(items))
    # for i in items:
    #     print(i['name'])
    if not items:
        logFile.write('No files found.')
        print('No files found.')
        return None
    else:
        # print('Files:')
        for item in items:
            # print(item['name'])
            if(item['name'] == FileName):
                print(FileName + " is already there")
                logFile.write(FileName + " is already there")
                # print(item['name'])
                return item['id']
def CopyToFolder(folderId,name):
    # Find Bata File
    MasterFile = CheckFileDir("Masterfile")
    # Find sector if not then create
    # sector = CreateFolder(folder)
    newfile = {'name': name,'parents' : [ folderId ]}
    service.files().copy(fileId=MasterFile, body=newfile).execute()
    print("Success copying file")
    logFile.write("\nSuccess copying file")

def MoveToFolder(folderId,fileId):
    # Find Bata File
    # Find sector if not then create
    # sector = CreateFolder(folder)
    newfile = {'parents' : [ folderId ]}
    service.files().move(fileId=fileId, body=newfile).execute()
    print("Success copying file")
    logFile.write("\nSuccess copying file")


def CheckFolder(FileName):
    page_token = None
    # response = service.files().list(q="mimeType = 'application/vnd.google-apps.spreadsheet'",
    response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
    items = response.get('files', [])
    #     # Process change
    #     print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    # page_token = response.get('nextPageToken', None)
    # if page_token is None:
    #     break
    # for i in items:
    #     print(i['name'])
    if not items:
        print('No files found.')
        logFile.write('No files found.')
        return None
    else:
        # print('Files:')
        for item in items:
            # print(item['name'])
            if(item['name'] == FileName):
                logFile.write(FileName + " is already there")
                print(FileName + " is already there")
                # print(item['name'])
                return item['id']
def delete_file(file_id):
  """Permanently delete a file, skipping the trash.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
    service.files().delete(fileId=file_id).execute()
  except Exception as e:
    print('An error occurred: %s',e)
    logFile.write('An error occurred: %s',e)

def DriveProcess(filename,folder,stockId):    
    try:
        # Find sector if not then create
        Filename = filename
                # Find sector if not then create
        sectorId = CheckFolder(folder)
        IsFileThere = CheckFileDir(Filename)
        if(sectorId == None):
            sectorId = CreateFolder(folder,stockId)
        else:
            pass
        if(IsFileThere == None):
            CopyToFolder(sectorId,Filename)
        else:
            logFile.write( Filename + " is already there")
            print( Filename + " is already there")
        
    except Exception as e:
        logFile.write("\n"+str(e))
        print(e)
        logFile.write("\nfail to process")
        print("fail to process")

