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


folder = "Food Process"

# def CopyFile(service,"Bata India Ltd"):


def CreateFolder(folder):
    # Call the Drive v3 API
    CheckFileDir(folder)
    print("folder/File is not there creating one...")
    file_metadata = {
    'name': folder,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s'% file.get('id'))
    return file.get('id')
    # print(u'{0}'.format(item['name']))

def CheckFileDir(FileName):
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # print(len(items))
    if not items:
        print('No files found.')
        return None
    else:
        # print('Files:')
        for item in items:
            # print(item['name'])
            if(item['name'] == FileName):
                print("folder/File is already there")
                # print(item['name'])
                return item['id']
def CopyToFolder(folderId,name):
    # Find Bata File
    BataFile = CheckFileDir("Bata India Ltd")
    # Find sector if not then create
    # sector = CreateFolder(folder)
    newfile = {'name': name,'parents' : [ folderId ]}
    service.files().copy(fileId=BataFile, body=newfile).execute()
    print("Success copying file")

def DriveProcess(filename,folder):    
    try:
        # Find sector if not then create
        Filename = filename
                # Find sector if not then create
        sectorId = CheckFileDir(folder)
        IsFileThere = CheckFileDir(Filename)
        if(sectorId == None):
            sectorId = CreateFolder(folder)
        else:
            pass
        if(IsFileThere == None):
            CopyToFolder(sectorId,Filename)
        else:
            print("File is already there")
        
    except Exception as e:
        print(e)
        print("fail to process")

