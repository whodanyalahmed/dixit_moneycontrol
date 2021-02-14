from selenium import webdriver
from screen import GatherData
from spread import updateNSE,GetLinks,UpdateCF,UpdateLink
from Drive import DriveProcess,CheckFileDir,delete_file,CreateFolder
from selenium.common.exceptions import TimeoutException
import time,sys,os
# import pandas as pd
# from screen import FillNames,url
from sys import platform
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
    # Windows...
# print("\n\nProcessing.....")
Replace = input("Do you want to replace files? (y/n)")
Replace = Replace.lower()
if(Replace == "y"):
    Replace_Bool = True
else:
    Replace_Bool = False
driver =webdriver.Chrome(path)
def getYear():
    driver.execute_script("window.scrollTo(0, 700)") 
    return driver.find_element_by_xpath("//div[@id='standalone-new']/div[1]/table/tbody/tr[1]/td[2]")
def getNextPageUrl():
    driver.execute_script("window.scrollTo(0, 700)") 
    url = driver.find_element_by_css_selector('span.nextpaging')
    url  = url.find_element_by_xpath('..').get_attribute('href')
    return url
def Find_links(name,urls):
    pair_links = []
    for url in urls:
        # print(url)
        if name in url:
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
                print("error : cant find next page or " + str(e))
                standAloneL.append(None)

        except Exception as e:
            print("error : cant find standalone years "+str(e))
            standAloneL.append(None)
            standAloneL.append(None)
        
        try:
            driver.find_element_by_id("#consolidated").click()
        except Exception as e:
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
                print("error : cant find next page or " + str(e))
                ConsoledatedL.append(None)

        except Exception as e:
            print("info : cant find consoledated years "+str(e))
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
    stockId = CheckFileDir("Stocks")
    if(stock == None):
        stockId = CreateFolder("Stocks")
    else:
        pass
except Exception as e:
    print(e)
companyName_link = GatherData()
# for n in range(len(companyName_link)):
index = 4
name = companyName_link[0][index]
print(name)
try:
    if(Replace_Bool):
        fileId = CheckFileDir(name)
        delete_file(fileId)
        print("success: deleted old file")
    else:
        pass
except Exception as e:
    print(e)
try:
    driver.get("https://www.moneycontrol.com/india/stockpricequote/" + name[0])
    print("success : Loaded...")
except TimeoutException as e:
    print("info : website taking too long to load...stopped")
    # driver.refresh()


# for d in data:    
nameList = name.split(" ")
links = []
PagesLink = []
try:
    try:
        normalName = driver.find_elements_by_partial_link_text(name)
        # print(len(normalName))
        normalName[0].click()
    except Exception as e:
        for e in reversed(nameList):
            # print("in namelist for loop")
            # link = driver.find_element_by_xpath(f"//*[contains(text(), '" + name.replace(e," ")  +"')]").click()
            tempname = name.replace(e,"")
            tempname = tempname.strip().split(" ")
            nameL = []
            for c in tempname:
                n = c.capitalize()
                n = n.replace(".","")
                nameL.append(n)
            tempname = " ".join(nameL) 
            # print(tempname)
            try:
                link = driver.find_element_by_partial_link_text(tempname)
                links.append(link)
            # print(links)
            except Exception as e:
                print(e)
            # if(len(links) <= 0 ):
            #     link = driver.find_element_by_partial_link_text(shortcode)
            #     links.append(link)    
    # driver.find_element_by_partial_link_text(name).click()
        try:
            links[0].click()
        except Exception as e:
            print("error : cant find the name " + str(e))    
    # time.sleep(4)
    try:
        sector = driver.find_element_by_xpath('//div[@id="stockName"]/span/strong').text
        print(sector)
    except Exception as e:
        print("error : cant find sector ")
    HomePage = driver.current_url
    PagesLink.append(HomePage)

    driver.set_page_load_timeout(50)
    time.sleep(3)

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)
    try:
        Bs = driver.find_element_by_xpath("//a[@title='Balance Sheet']")
        Bsurl = Bs.get_attribute('href')
        driver.get(Bsurl)
        ConOrSta(PagesLink)
        print("success : fetched Balance Sheet")

    except Exception as e:
        print("error : cant find balance sheet ")
    try:
        nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[2]").text
        if(nse == "" or nse == None):
            nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[1]").text
    except Exception as e:
        print("info : cant find NSE "+str(e))
        nse = driver.find_element_by_xpath("//p[contains(@class, 'bsns_pcst ') and contains(@class, 'disin')]/ctag/span[1]").text
    # print(nse)
    SpreadsheetId = CheckFileDir(name)

    if(SpreadsheetId == None):
        print("file is not already there creating one")
        DriveProcess(name,sector,stockId)
        SpreadsheetId = CheckFileDir(name)
    else:
        print("file is already there")
    Nse_string= str(nse).upper()
    # print(SpreadsheetId)
    # print(Nse_string)
    try:

        updateNSE(Nse_string,SpreadsheetId)
    except Exception as e:
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
        print(e)

    time.sleep(3)
    try:
        Pl = driver.find_element_by_xpath("//a[@title='Profit & Loss' and @class='ProfitLoss']")
        PLurl = Pl.get_attribute('href')
        driver.get(PLurl)
        ConOrSta(PagesLink)
        print("success : fetched Profit and Loss")

    except Exception as e:
        print("Cant find profit loss or " + str(e))
    try:
        ProfitLossLinks = Find_links("profit",PagesLink)
        populatePairValues(ProfitLossLinks,3,4)
    except Exception as e:
        print(e)
    # Querterly report
    
    # time.sleep(3)

    try:
        Qr = driver.find_element_by_xpath("//a[@title='Quarterly Results' and @class='QuarterlyResults']")
        Qrurl = Qr.get_attribute('href')
        driver.get(Qrurl)
        ConOrSta(PagesLink)
        print("success : fetched Quarterly Report")

    except Exception as e:
        print("Cant find Qurarterly report or " + str(e))
    try:
        QuarterlyLinks = Find_links("quarterly",PagesLink)
        populatePairValues(QuarterlyLinks,5,6)
    except Exception as e:
        print(e)
    # cash flow
    try:
        Cf = driver.find_element_by_xpath("//a[@title='Cash Flows' and @class='CashFlows']")
        Cfurl = Cf.get_attribute('href')
        driver.get(Cfurl)
        ConOrSta(PagesLink)
        print("success : fetched Cash Flow")

    except Exception as e:
        print("Cant find Cash flow or " + str(e))
    try:
        CashFlowLinks = Find_links("cash",PagesLink)
        populatePairValues(CashFlowLinks,7,8)
    except Exception as e:
        print(e)
    # Capital Structure
    # time.sleep(3)
    
    try:
        Cf = driver.find_element_by_xpath("//a[@title='Capital Structure' and @class='CapitalStructure']")
        Cfurl = Cf.get_attribute('href')
        PagesLink.append(Cfurl)
        print("success : fetched Capital Structure")
    except Exception as e:
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
        print("error : cant get screener url or " + str(e))
    try:
        ScreenerLinks = Find_links("screener",PagesLink)
        populateSingleValues(ScreenerLinks,13)
    except Exception as e:
        print(e)
    print(values)
    try:
        UpdateLink(SpreadsheetId,values)
    except Exception as e:
        print(e)
#   CF screener
    try:
        driver.get(screener_url)
        driver.find_element_by_xpath("//section[@id='cash-flow']/div[2]/table/tbody/tr[2]/td[1]/button").click()
        time.sleep(5)
        cf = driver.find_element_by_xpath("//section[@id='cash-flow']/div[2]/table/tbody/tr[3]").text
        cf = str(cf).split(' ')
        cf = cf[3:]
        print(cf)
    except Exception as e:
        print(e)

    if(len(cf) >= 10 ):
        cf = cf[-10:]
    else:
        len_cf = len(cf)
        remaining = 10-len_cf
        d_list = [' ']*remaining
        for e in d_list:
            cf.append(e)
    cf_format = []
    cf_format.append(cf)
    print(cf_format)
    try:
        UpdateCF(SpreadsheetId,cf_format)
    except Exception as e:
        print(e)
except Exception as e:
    print("Something went wrong" + str(e))


# print(PagesLink)

print("success : complete")