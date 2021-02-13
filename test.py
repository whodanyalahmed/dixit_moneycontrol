from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
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


    folder = "Pharma"

    # def CopyFile(service,"Bata India Ltd"):

    def CreateFolder(service,folder):
        # Call the Drive v3 API
        results = service.files().list(fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        # print(len(items))
        if not items:
            print('No files found.')
        else:
            # print('Files:')
            for item in items:
                if(item['name'] == folder):
                    print("folder is already there")
                    print(item['name'])
                    return item['id']
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


    try:
        BataFile = CreateFolder(service,"Bata India Ltd")
        PharmaId = CreateFolder(service,folder)
        newfile = {'name': "BataFile",'parents' : [ { "id" : PharmaId } ]}
        service.files().copy(fileId=BataFile, body=newfile).execute()
        print("Success")
    except Exception as e:
        print(e)
        print("fail")

if __name__ == '__main__':
    main()