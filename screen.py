from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import time,sys,os
# import selenium
# from selenium import webdriver

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.dirname(__file__)
#     return os.path.join(base_path, relative_path)

# path = resource_path('I://clients//chromedriver.exe')
        
# print("\n\nProcessing.....")
# options = webdriver.ChromeOptions()
# options.add_argument('--disable-extensions')
# options.add_argument('--profile-directory=Default')
# # options.add_argument("--incognito")
# options.add_argument("--disable-plugins-discovery")
# options.add_argument("--start-maximized")
# # options.add_argument('headless')
# driver =webdriver.Chrome(path,options=options)



def MakeSoup(object):
    soup = BeautifulSoup(object,'lxml')
    return soup

print("Processing....")

logFile = open("log.txt","a+")

# tb = soup.find_all('table')
companies = []
urls = []
main= []
full_company = []
url = input("Enter screener url: ").lower()
run = input("Run from center(y/n):  ").lower()
bnse = []

# url= "https://www.screener.in/screens/265380/Good-Solvent-Growth-companies"
# url= "https://www.screener.in/screens/282622/Solvency-Screen/"
# url= "https://www.screener.in/screens/178/Growth-Stocks/"
# url= "https://www.screener.in/screens/59/Magic-Formula/"
# https://www.screener.in/screens/330165/Good-Companies-for-Investing/
# https://www.screener.in/screens/86/quarterly-growers/
# https://www.screener.in/screens/3/highest-dividend-yield-shares/
c = 0
z= 0
flag = 0
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
headers = { 
	'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
}
cookie = ""

def Fill_data(url):
    FillNames(url)
    # print(url)
    try:
        # s = requests.Session()
        # s.headers.update(headers)

        # req = s.get("https://www.screener.in")
        # cookie = req.cookies
        # print(str(dict(cookie)))
        for e in urls:

            html = requests.get("https://www.screener.in" + e,stream=True).content
            
            # req = Request("https://www.screener.in" + e,headers={'User-Agent': 'Mozilla/5.0'})
            # html = urlopen(req).read()
            soup = MakeSoup(html)
            # find top
            top = soup.findChild("div",{"id":"top"})
            # find bse or nse
            # print(top)
            try:
                company_links = soup.find_all("div",{"class":"company-links"})[0]
            except Exception as error:
                print("again trying..." + e)
                time.sleep(1)
                # req = Request("https://www.screener.in" + e,headers=headers)
                # html = urlopen(req).read()
                html = requests.get("https://www.screener.in" + e).content
                soup = MakeSoup(html)
                # find top
                top = soup.findChild("div",{"id":"top"})
                try:
                    company_links = soup.find_all("div",{"class":"company-links"})[0]
                except Exception as err:
                    print(err)
                    continue
                print(error)
            company_soup = MakeSoup(str(company_links))
            top_div = MakeSoup(str(top))
            top_div_str = top_div.find_all("div",{'class': 'flex-row'})
            top_h1 = MakeSoup(str(top_div_str))
            ful_com = top_h1.find("h1",{'class':'margin-0'}).text
            # print(ful_com)
            full_company.append(ful_com)
            se = company_soup.find_all("span",{"class":['ink-700','upper']})
            # print(se)
            # if 'BSE' in str(se):
            #     for un in se:
            #         if 'BSE' in un.text:
            #             print('in bse')
            #             nse = un.text.split(":")[1]
            #             nse = nse.replace(" ","")
            #             nse = nse.replace("\n","")
            #             bnse.append(nse)
            #             break
            # elif 'NSE' in str(se):
            #     for unkown in se:    
            #         if 'NSE' in unkown.text:
            #             print("in NSE")
            #             bse = unkown.text.split(":")[1]
            #             bse = bse.replace(" ","")
            #             bse = bse.replace("\n","")
            #             bnse.append(bse)

            #             break
            # else:
            #     print("cant find NSE or BSE")
            #     logFile.write("\ncant find NSE or BSE")
            #     bnse.append(None)
            try:
                try:
                    for un in se:
                        if 'BSE' in un.text:
                            # print("found BSE")
                            try:
                                nse = un.text.split(":")[1]
                            except Exception as e:
                                print("exception in BSE")
                            nse = nse.replace(" ","")
                            nse = nse.replace("\n","")
                            bnse.append(nse)
                            print(nse)
                except Exception as err:
                    raise Exception("Cant find BSE")
            except Exception as error:
                print(error)
                for unkown in se:    
                    if 'NSE' in unkown.text:
                        print("found NSE")
                        try:
                            bse = unkown.text.split(":")[1]
                        except Exception as e:
                                print("exception in NSE")
                        # print(bse)
                        bse = bse.replace(" ","")
                        bse = bse.replace("\n","")
                        bnse.append(bse)
                        print(bse)
                        break
                    else:
                        print("cant find NSE or BSE")
                        bnse.append(None)
            global z
            print(e)
            print(z)
            z+=1

    except Exception as e:
        print("some error here " +str(e))
        logFile.write("\n"+str(e))
    main.append(companies)
    main.append(urls)
    main.append(full_company)
    main.append(bnse)
    # print(len(bnse))
    # print(len(full_company))
    print("len of company: "+ str(len(companies)))
    print("len of urls: " + str(len(urls)) )
    print("len of full company: " + str(len(full_company)))
    print("len of BNSE: " + str(len(bnse)) )
    
    logFile.write("\nGot all the names from screener")
    print("Got all the names from screener")

    return main

def GoNextPage(page,*url):
    if(page == 0):
        pass
    else:
        print(url[0] + "/" + page)
        FillNames(url[0] + "/" + page)



def FillNames(url):
    # url = str(url).lower()
    # print(url)
    # url = str(url).replace('www.','')
    
    # html = driver.get(url)
    # print("url is: " + url)
    # print("current url is: " + driver.current_url )
    # while True:
    #     if(driver.current_url == url):
    #         print('in if')
    #         break
    #     else:
    #         print('in else')
    #         html = driver.get(url)


    # time.sleep(2)
    # html = driver.page_source

    html = requests.get(url).content
    soup = MakeSoup(html)
    input_tag = soup.find_all('tr')
    for a in input_tag:
        company_name = a.get('data-row-company-name')
        tr_soup = MakeSoup(str(a))
        # print(tr_soup)
        company_url  = tr_soup.find('a').get('href')
        com = str(company_url).strip('/')
        com = com.split('/')[0]
        # print(com)
        if(com == "company"):
            urls.append(company_url)
        else:
            pass
        if(company_name == None):
            pass    
        else:
            companies.append(company_name)
    global c
    # print(c)
    if(c == 0 and run == 'n'):
        # print('in if')
        op = soup.find('div',{'class': 'options'})
        # print(op)

        try:
            a = op.find_all('a')
            NextPage = a[0]['href']
            # print(NextPage)
            # FillNames(url+NextPage)
            # return NextPage
            c+=1
            GoNextPage(NextPage,url)
        except Exception as e:
            print("Cant find page or pages are ended " + str(e))
            logFile.write("\nCant find page or pages are ended " + str(e))
            GoNextPage(0)

            # return 0
        
    else:
        # print("in else")
        op = soup.find_all('div',{'class': 'options'})
        # print(op)

        try:
            if(len(op) == 3):
                a = op[1].find_all('a')
                NextPage = a[0]['href']
                # print(NextPage)
                url = url.split("?")
                # print(url)
                url = url[0]
                # print(url)
                url = url[:-1]
                # print(url)
                GoNextPage(NextPage,url)
            else:
                # print("ending loop ")
                GoNextPage(0)
        except Exception as e:
            print("Cant find page or pages are ended " + str(e))
            logFile.write("\nCant find page or pages are ended " + str(e))
def GatherData():
    d = Fill_data(url)
    # print(d)
    return d

# d = Fill_data(url)
# print(d[1])
# print(len(d[1]))

# for e in range(len(companies)):
#     print(str(e+1) + " - "  + companies[e])

