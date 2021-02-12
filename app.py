from selenium import webdriver
from screen import GatherData
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
driver =webdriver.Chrome(path)
def getYear():
    driver.execute_script("window.scrollTo(0, 700)") 
    return driver.find_element_by_xpath("//div[@id='standalone-new']/div[1]/table/tbody/tr[1]/td[2]")
def getNextPageUrl():
    url = driver.find_element_by_css_selector('span.nextpaging')
    url  = url.find_element_by_xpath('..').get_attribute('href')
    return url

def ConOrSta(li):
        standAloneL = []
        ConsoledatedL = []
        di = {}
        try:
            standAlone = getYear()
            print(standAlone.text)
            standAloneYear_url = driver.current_url
            standAloneL.append(standAloneYear_url)
            try:
                print("info : Comma one...")
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
            print(Consoledated.text)
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
            print("error : cant find consoledated years "+str(e))
            ConsoledatedL.append(None)
            ConsoledatedL.append(None)
        # print(type(di['consoledated']))
        # print(int(di['consoledated']))
        # print(int(di['standalone']))
        if(int(di['consoledated']) < int(di['standalone'])):
            print("standalone")
            for d in standAloneL:
                li.append(d)
        else:
            print("consoledated")
            for d in ConsoledatedL:
                li.append(d)
        
driver.maximize_window()
# open link
# driver.set_page_load_timeout(120)
driver.set_page_load_timeout(30)

# data = pd.read_csv("Equity.csv")
# data = data['Security Id'] 
shortcode = "HDFC"
name = GatherData()
name = name[0]
print(name)
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
        print(len(normalName))
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
                nameL.append(n)
            tempname = " ".join(nameL) 
            # print(tempname)
            try:
                link = driver.find_element_by_partial_link_text(tempname)
                links.append(link)
            # print(links)
            except Exception as e:
                print(e)
            if(len(links) <= 0 ):
                link = driver.find_element_by_partial_link_text(shortcode)
                links.append(link)    
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
    PagesLink.append(driver.current_url)
    try:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)
        BS = driver.find_element_by_xpath("//a[@title='Balance Sheet']")
        driver.get(BS.get_attribute('href'))
    except Exception as e:
        print("error : cant find balance sheet ")
    # print("waiting")
    # time.sleep(10)
    # print("changing tab")
    # driver.switch_to.window(driver.window_handles[0])
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    # driver.set_script_timeout(60)
    driver.set_page_load_timeout(50)

    ConOrSta(PagesLink)

    # try:
    #     standAlone = getYear()
    #     standAloneYear_url = driver.current_url
    #     standAloneL.append(standAloneYear_url)
    #     di['standalone'] = standAlone.text.split(" ")[1]
    #     # print(di['standalone'] + " and waiting")
    #     # time.sleep(10)
    #     # standAlone_url2 = driver.find_element_by_xpath("//ul[@class='pagination']")
    #     try:
    #         standAloneYear_url2 = getNextPageUrl()
    #         standAloneL.append(standAloneYear_url2)
    #     except Exception as e:
    #         print("error : cant find next page or " + str(e))
    #         standAloneL.append(None)

    # except Exception as e:
    #     print("error : cant find standalone years "+str(e))
    #     standAloneL.append(None)
    #     standAloneL.append(None)
    
    # try:
    #     driver.find_element_by_id("#consolidated").click()
    # except Exception as e:
    #     print("error : cant find consoledated link "+str(e))
    
    # # print("waiting")
    # # time.sleep(5)
    
    # try:
    #     Consoledated = getYear()
    #     Consoledated_url = driver.current_url
    #     ConsoledatedL.append(Consoledated_url)
    #     di['consoledated']  = Consoledated.text.split(" ")[1]
    #     # print(di['consoledated'] + " and waiting")
    #     # time.sleep(10)
    #     # consoledated_url2 = driver.find_element_by_xpath("//ul[@class='pagination']/")
    #     try:
    #         consoledated_url2 = getNextPageUrl()
    #         ConsoledatedL.append(consoledated_url2)
    #     except Exception as e:
    #         print("error : cant find next page or " + str(e))
    #         ConsoledatedL.append(None)

    # except Exception as e:
    #     print("error : cant find consoledated years "+str(e))
    #     ConsoledatedL.append(None)
    #     ConsoledatedL.append(None)
    # print(type(di['consoledated']))
    # if(int(di['consoledated']) < int(di['standalone'])):
    #     print("standalone")
    #     for d in standAloneL:
    #         PagesLink.append(d)
    # else:
    #     print("consoledated")
    #     for d in ConsoledatedL:
    #         PagesLink.append(d)
    # Profit and loss
    try:
        Pl = driver.find_element_by_xpath("//a[@title='Profit & Loss' and @class='ProfitLoss']")
        PLurl = Pl.get_attribute('href')
        driver.get(PLurl)
        ConOrSta(PagesLink)

        # PagesLink.append(PLurl)
        # try:
        #     PL_url2 = getNextPageUrl()
        #     # print(PL_url2)
        #     PagesLink.append(PL_url2)
        # except Exception as e:
        #     print("error : cant find next PL page or " + str(e))
        #     PagesLink.append(None)
    except Exception as e:
        print("Cant find profit loss or " + str(e))
    # Querterly report
    try:
        Qr = driver.find_element_by_xpath("//a[@title='Quarterly Results' and @class='QuarterlyResults']")
        Qrurl = Qr.get_attribute('href')
        driver.get(Qrurl)
        ConOrSta(PagesLink)
        # PagesLink.append(Qrurl)
        # try:
        #     Qr_url2 = getNextPageUrl()
        #     # print(Qr_url2)
        #     PagesLink.append(Qr_url2)
        # except Exception as e:
        #     print("error : cant find next QR page or " + str(e))
        #     PagesLink.append(None)
    except Exception as e:
        print("Cant find Qurarterly report or " + str(e))
    # cash flow
    try:
        Cf = driver.find_element_by_xpath("//a[@title='Cash Flows' and @class='CashFlows']")
        Cfurl = Cf.get_attribute('href')
        driver.get(Cfurl)
        ConOrSta(PagesLink)

        # PagesLink.append(Cfurl)
        # try:
        #     Cf_url2 = getNextPageUrl()
        #     # print(Cf_url2)
        #     PagesLink.append(Cf_url2)
        # except Exception as e:
        #     print("error : cant find next Cf page or " + str(e))
        #     PagesLink.append(None)
    except Exception as e:
        print("Cant find Cash flow or " + str(e))

except Exception as e:
    print("Something went wrong" + str(e))

print(PagesLink)
print("success : complete")