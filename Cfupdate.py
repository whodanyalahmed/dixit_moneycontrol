import datetime
import pickle,os.path,datetime,time,sys
from selenium import webdriver
from sys import platform
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium.webdriver.chrome.options import Options
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


if platform == "linux" or platform == "linux2":
    # linux
    path = resource_path('driver/chromedriver')
else:
    path = resource_path('driver/chromedriver.exe')
# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.headless = True # also works
# driver = webdriver.Chrome()
    # Windows...
print("\n\nProcessing.....")

# driver =webdriver.Chrome(path,options=chrome_options)
driver =webdriver.Chrome(path)
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
logFile = open("CfProgramLog.txt","a+")

logFile.write("\nStarted at: " + str(datetime.datetime.now()))
names = []
ids = []



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
        # logFile.write("\nsuccess: Excel Readable found")
        # print('success: Excel Readable found')
        return values
def GetLink(Id):
    Links_Range = "B18:B18"
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


def UpdateTheValues (folder_id):
    try:
        results = service.files().list(q="'{}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet'".format(folder_id),spaces='drive',fields="nextPageToken, files(id, name)",pageSize=400).execute()
        items = results.get('files', [])
        # print(items)
        for item in items:
            print("Name: " + item['name'] + " Id: " +item['id'] )
            names.append([item['name']])
            # start of get link code
            time.sleep(2)
            try:
                d = GetLink(item['id'])
                screener_link = d[0][0]
                if screener_link != ".":
                    getupdateCfValues(screener_link,item['id'])
                    
                    print("success : updated link of " + str(item['name']) + "\n" )
                    logFile.write("\nsuccess : updated link of " + str(item['name']) )
                else:
                    print("info : no link found")
                    logFile.write("\ninfo : no link found")
            except Exception as e:
                print(e)
            # End of getLink code
            ids.append([item['id']])
    
    except Exception as e:
        print(e)

def getupdateCfValues(url,id):
    try:
        driver.get(url)
        driver.find_element_by_xpath("//section[@id='cash-flow']/div[2]/table/tbody/tr[2]/td[1]/button").click()
        time.sleep(5)
        cf = driver.find_element_by_xpath("//section[@id='cash-flow']/div[2]/table/tbody/tr[3]").text
        cf = str(cf).split(' ')
        cf = cf[3:]
        # print(cf)
    except Exception as e:
        logFile.write("\n"+str(e))
        print(e)

    if(len(cf) >= 10 ):
        cf = cf[-10:]
    else:
        len_cf = len(cf)
        remaining = 10-len_cf
        d_list = [' ']*remaining
        for e in d_list:
            cf.insert(0,e)
    cf_format = []
    cf_format.append(cf)
    # print(cf_format)
    try:
        UpdateCF(id,cf_format)
    except Exception as e:
        print(e)
        logFile.write("\n"+str(e))

def CheckFolder(FileName):
    page_token = None
    # response = service.files().list(q="mimeType = 'application/vnd.google-apps.spreadsheet'",
    response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
    items = response.get('files', [])

    if not items:
        print('No files found.')
        logFile.write('\nNo files found.')
        return None
    else:
        # print('Files:')
        for item in items:
            # print(item['name'])
            if(item['name'] == FileName):
                logFile.write("\n"+FileName + " is already there")
                print(FileName + " is already there")
                # print(item['name'])
                return item['id']


# Range = "Online Entry!"

stocks_id = CheckFolder("Stocks")
UpdateTheValues(stocks_id)

# try:
#     d = GetLink(ids[0])
#     print(d)
# except Exception as e:
#     print(e)

# for id in ids:
#     try:
#         d = getCfLink(id)
#         print(d)
#     except Exception as e:
#         print(e)