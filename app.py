import datetime
from selenium import webdriver
from screen import GatherData
from spread import updateNSE,GetLinks,UpdateCF,UpdateLink
from Drive import CheckFolder, DriveProcess,CheckFileDir,delete_file,CreateFolder
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
import time,sys,os
from sys import platform
logFile = open("log.txt","a+")
logFile.write("\nStarted at: " + str(datetime.datetime.now()))
cur_path = sys.path[0]
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
# print("\n\nProcessing.....")
Replace = input("Do you want to replace files? (y/n) : ")
Replace = Replace.lower()
if(Replace == "y"):
    Replace_Bool = True
else:
    Replace_Bool = False
# driver =webdriver.Chrome(path,options=chrome_options)
driver =webdriver.Chrome(path)

def getYear():
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 700)")
    return driver.find_element_by_xpath("//div[@id='standalone-new']/div[1]/table/tbody/tr[1]/td[2]")
def getNextPageUrl():
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 700)") 
    url = driver.find_element_by_css_selector('span.nextpaging')
    url  = url.find_element_by_xpath('..').get_attribute('href')
    return url
def Find_links(name,urls):
    pair_links = []
    for url in urls:
        # print(url)
        if name in url:
            logFile.write("\nfound " + str(name))
            print("found " + name)
            pair_links.append(url)
    if(len(pair_links) == 0):
        pair_links = [None,None]
    return pair_links
def ConOrSta(li):
        standAloneL = []
        ConsoledatedL = []
        di = {}
        try:
            standAlone = getYear()
            standAloneYear_url = driver.current_url
            standAloneL.append(standAloneYear_url)
            try:
                # print("info : Comma one...")
                di['standalone'] = standAlone.text.split("'")[1]
            except Exception as e:
                di['standalone'] = standAlone.text.split(" ")[1]
            # print(di['standalone'] + " and waiting")
            # time.sleep(10)
            # standAlone_url2 = driver.find_element_by_xpath("//ul[@class='pagination']")
            try:
                standAloneYear_url2 = getNextPageUrl()
                standAloneL.append(standAloneYear_url2)
            except Exception as e:
                logFile.write("\nerror : cant find next page or " + str(e))
                print("error : cant find next page or " + str(e))
                standAloneL.append(None)

        except Exception as e:
            logFile.write("\nerror : cant find standalone years "+str(e))
            print("error : cant find standalone years "+str(e))
            standAloneL.append(None)
            standAloneL.append(None)
        
        try:
            driver.find_element_by_id("#consolidated").click()
        except Exception as e:
            logFile.write("\nerror : cant find consoledated link "+str(e))
            print("error : cant find consoledated link "+str(e))
        
        try:
            Consoledated = getYear()
            Consoledated_url = driver.current_url
            ConsoledatedL.append(Consoledated_url)
            try:
                # print("info : Comma one...")
                di['consoledated']  = Consoledated.text.split("'")[1]
            except Exception as e:
                di['consoledated']  = Consoledated.text.split(" ")[1]
            # print(di['consoledated'] + " and waiting")
            # time.sleep(10)
            # consoledated_url2 = driver.find_element_by_xpath("//ul[@class='pagination']/")
            try:
                consoledated_url2 = getNextPageUrl()
                ConsoledatedL.append(consoledated_url2)
            except Exception as e:
                logFile.write("\nerror : cant find next page or " + str(e))
                print("error : cant find next page or " + str(e))
                ConsoledatedL.append(None)

        except Exception as e:
            # print("info : cant find consoledated years "+str(e))
            if(len(standAloneL) == 2):
                for e in standAloneL:
                    ConsoledatedL.append(e)
            else:
                ConsoledatedL.append(None)
                ConsoledatedL.append(None)
        # print(type(di['consoledated']))
        # print(int(di['consoledated']))
        # print(int(di['standalone']))\
        try:
            if(int(di['consoledated']) < int(di['standalone'])):
                # print("standalone")
                for d in standAloneL:
                    li.append(d)
            else:
                for d in ConsoledatedL:
                    li.append(d)
        except Exception as e:
            # print("consoledated")
            for d in ConsoledatedL:
                    li.append(d)
            
driver.maximize_window()
# open link
# driver.set_page_load_timeout(120)
driver.set_page_load_timeout(30)

# data = pd.read_csv("Equity.csv")
# data = data['Security Id'] 
# shortcode = "HDFC"

try:
    stockId = CheckFolder("Stocks")
    if(stockId == None):
        stockId = CreateFolder("Stocks")
    else:
        pass
except Exception as e:
    logFile.write("\n"+str(e))
    print(e)
companyName_link = GatherData()
no_of_companies = len(companyName_link[0])
logFile.write(str(no_of_companies))
print(no_of_companies)
for index in range(no_of_companies):
    # index = 4
    name = companyName_link[2][index]
    # print(name)
    try:
        fileId = CheckFileDir(name)
        if(fileId == None):
            pass
        else:
            if(Replace_Bool):
                delete_file(fileId)
                logFile.write("\nsuccess: deleted old file")
                print("success: deleted old file")
            else:
                # print("info : skipping element already there")
                continue
    except Exception as e:
        logFile.write("\n"+str(e))
        print(e)
    try:
        driver.get("https://www.moneycontrol.com/india/stockpricequote/" + name[0])
        logFile.write("\nsuccess : Loaded...")
        print("success : Loaded...")
    except TimeoutException as e:
        logFile.write("\ninfo : website taking too long to load...stopped")
        print("info : website taking too long to load...stopped")
        # driver.refresh()


    # for d in data:    
    nameList = companyName_link[0][index].split(" ")
    links = []
    PagesLink = []
    
    nse = companyName_link[3][index]
    try:
        print("Trying BSE of : " + name )
        logFile.write("\nTrying BSE of : " + name )
        try:
            search_inp = driver.find_element_by_id("search_str")
            search_inp.send_keys(nse)
            search_inp.send_keys(Keys.ENTER)
            try:
                driver.find_element_by_id("proceed-button").click()
                print("success : clicked send anyway")
                logFile.write("success : clicked send anyway")
            except Exception as e:
                print(e)
                logFile.write("\n"+str(e))
                
        except Exception as error:
            print(error+ " cant find: " + nse)
            logFile.write("\n"+str(error) + "cant find: " + nse)
        # time.sleep(3)
        # try:
        #     sector = driver.find_element_by_xpath('//div[@id="stockName"]/span/strong').text
        #     logFile.write("\n"+sector)
        #     print(sector)
        # except Exception as e:
        #     logFile.write("\nerror : cant find sector ")
        #     print("error : cant find sector ")
        HomePage = driver.current_url
        PagesLink.append(HomePage)

        driver.set_page_load_timeout(50)
        time.sleep(3)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)
        try:
            def findBalancesheet():
                Bs = driver.find_element_by_xpath("//a[@title='Balance Sheet']")
                Bsurl = Bs.get_attribute('href')
                driver.get(Bsurl)
                time.sleep(5)
                ConOrSta(PagesLink)
                logFile.write("\nsuccess : fetched Balance Sheet")
                print("success : fetched Balance Sheet")
            findBalancesheet()
        except Exception as e:
            driver.refresh()
            logFile.write("\nTrying again to find Balance Sheet")
            print("Trying again to find Balance Sheet")
            findBalancesheet()
            logFile.write("\nerror : cant find balance sheet ")
            print("error : cant find balance sheet ")
        # try:
        #     nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[2]").text
        #     if(nse == "" or nse == None):
        #         nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[1]").text
        # except Exception as e:
        #     print("info : cant find NSE "+str(e))
        #     driver.refresh()
        #     time.sleep(2)
        #     nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[1]").text
        # print(nse)
        SpreadsheetId = CheckFileDir(name)
        try: 
            if(SpreadsheetId == None):
                logFile.write("\nfile is not already there creating one")
                print("file is not already there creating one")
                DriveProcess(name,stockId)
                SpreadsheetId = CheckFileDir(name)
            else:
                logFile.write("\nfile is already there")
                print("file is already there")
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        Nse_string= str(nse).upper()
        # print(SpreadsheetId)
        # print(Nse_string)
        try:

            updateNSE(Nse_string,SpreadsheetId)
        except Exception as e:
            logFile.write("\nerror : cant update ")
            logFile.write("\n"+str(e))
            print("error : cant update ")
            print(e)
        
        values = GetLinks(SpreadsheetId)
        values[0][0] = HomePage
        def populatePairValues(PairLinks,index1,index2):
            if(len(PairLinks) == 2):
                values[index1][0] = PairLinks[0]
                values[index2][0] = PairLinks[1]
            elif(len(PairLinks) == 1):
                values[index1][0] = PairLinks[0]
                values[index2][0] = None
            else:
                values[index1][0] = None
                values[index2][0] = None
        try:

            BalanceSheetLinks = Find_links("balance",PagesLink)
            populatePairValues(BalanceSheetLinks,1,2)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)

        time.sleep(3)
        try:
            def findProfitLoss():
                Pl = driver.find_element_by_xpath("//a[@title='Profit & Loss' and @class='ProfitLoss']")
                PLurl = Pl.get_attribute('href')
                driver.get(PLurl)
                ConOrSta(PagesLink)
                logFile.write("\nsuccess : fetched Profit and Loss")
                print("success : fetched Profit and Loss")
            findProfitLoss()
        except Exception as e:
            driver.refresh()
            logFile.write("\nTrying again to find Profit Loss")
            print("Trying again to find Profit Loss")
            findProfitLoss()
            logFile.write("\nCant find profit loss or " + str(e))
            print("Cant find profit loss or " + str(e))
        try:
            ProfitLossLinks = Find_links("profit",PagesLink)
            populatePairValues(ProfitLossLinks,3,4)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        # Querterly report
        
        # time.sleep(3)

        try:
            def findQuarReport():
                Qr = driver.find_element_by_xpath("//a[@title='Quarterly Results' and @class='QuarterlyResults']")
                Qrurl = Qr.get_attribute('href')
                driver.get(Qrurl)
                ConOrSta(PagesLink)
                logFile.write("\nsuccess : fetched Quarterly Report")
                print("success : fetched Quarterly Report")
            findQuarReport()
        except Exception as e:
            driver.refresh()
            logFile.write("\nTrying again to find Quarterly Report")
            print("Trying again to find Quarterly Report")
            findQuarReport()
            logFile.write("\nCant find Qurarterly report or " + str(e))
            print("Cant find Qurarterly report or " + str(e))
        try:
            QuarterlyLinks = Find_links("quarterly",PagesLink)
            populatePairValues(QuarterlyLinks,5,6)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        # cash flow
        try:
            def findCashFlow():
                Cf = driver.find_element_by_xpath("//a[@title='Cash Flows' and @class='CashFlows']")
                Cfurl = Cf.get_attribute('href')
                driver.get(Cfurl)
                ConOrSta(PagesLink)
                logFile.write("\nsuccess : fetched Cash Flow")
                print("success : fetched Cash Flow")
            findCashFlow()
        except Exception as e:
            driver.refresh()
            logFile.write("\nTrying again to find Cash flow")
            print("Trying again to find Cash flow")
            findCashFlow()
            logFile.write("\nCant find Cash flow or " + str(e))
            print("Cant find Cash flow or " + str(e))
        try:
            CashFlowLinks = Find_links("cash",PagesLink)
            populatePairValues(CashFlowLinks,7,8)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        # Capital Structure
        # time.sleep(3)
        
        try:
            def findCapStructure():
                Cs = driver.find_element_by_xpath("//a[@title='Capital Structure' and @class='CapitalStructure']")
                Csurl = Cs.get_attribute('href')
                PagesLink.append(Csurl)
                logFile.write("\nsuccess : fetched Capital Structure")
                print("success : fetched Capital Structure")
            findCapStructure()
        except Exception as e:
            driver.refresh()
            logFile.write("\nTrying again to find Capital Structure")
            print("Trying again to find Capital Structure")
            findCapStructure()
            logFile.write("\nCant find Capital Structure or " + str(e))
            print("Cant find Capital Structure or " + str(e))

        def populateSingleValues(PairLinks,index1):
            if(len(PairLinks) == 1):
                values[index1][0] = PairLinks[0]
            else:
                values[index1][0] = None
        try:
            CapitalLinks = Find_links("capital",PagesLink)
            populateSingleValues(CapitalLinks,9)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        # for screener
        try:
            screener_url = "https://www.screener.in" 
            com = companyName_link[1][index]
            screener_url = screener_url+com
            PagesLink.append(screener_url)
            # print(screener_url)
        except Exception as e:
            screener_url = None
            PagesLink.append(screener_url)
            logFile.write("\nerror : cant get screener url or " + str(e))
            print("error : cant get screener url or " + str(e))
        try:
            ScreenerLinks = Find_links("screener",PagesLink)
            populateSingleValues(ScreenerLinks,10)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        logFile.write(str(values))
        print(values)
        try:
            UpdateLink(SpreadsheetId,values)
        except Exception as e:
            print(e)
            logFile.write("\n"+str(e))
    #   CF screener
        try:
            driver.get(screener_url)
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
            UpdateCF(SpreadsheetId,cf_format)
        except Exception as e:
            print(e)
            logFile.write("\n"+str(e))
    except Exception as e:
        logFile.write("\nSomething went wrong " + str(e))
        print("Something went wrong" + str(e))
    # print(PagesLink)

logFile.write("\nsuccess : complete")
print("success : complete")

logFile.close()