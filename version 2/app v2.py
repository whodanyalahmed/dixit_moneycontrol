import datetime
from selenium import webdriver
from screen import GatherData
from spread import updateSingleValue, UpdateCF, UpdateLink
from Drive import CheckFolder, DriveProcess, CheckFileDir, delete_file, CreateFolder
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
# import webdriverwait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
import time
import sys
import os
from sys import platform
logFile = open("log.txt", "a+")
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
driver = webdriver.Chrome(path)


def getYear():
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 700)")
    return driver.find_element_by_xpath("//div[@id='standalone-new']/div[1]/table/tbody/tr[1]/td[2]")


def getNextPageUrl():
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 700)")
    url = driver.find_element_by_css_selector('span.nextpaging')
    url = url.find_element_by_xpath('..').get_attribute('href')
    return url


def get_table_row_data(name):
    li = []
    try:
        # find td with text 'Total Shareholders Funds' and its sibling tds
        # with text 'Total Shareholders Funds'

        driver.execute_script("window.scrollTo(0, 700)")
        tds = driver.find_elements_by_xpath(
            "//td[contains(text(),'"+name+"')]/following-sibling::td")
        print("info: "+name+" is available")
        for td in tds:

            print(td.text)
            if(td.text != " "):
                li.append(td.text)
        return li
    except Exception as e:
        print("error : cant find shareholder information")
        logFile.write("\nerror : cant find shareholder information")
        print(e)


def ConOrSta(li, url):
    standAloneL = []
    ConsoledatedL = []
    di = {}
    consoledated_total_shares_funds = []
    consoledated_long_term_borrowing = []
    consoledated_short_term_borrowing = []
    consoledated_cash_n_cash_eqi = []

    standalone_total_shares_funds = []
    standalone_long_term_borrowing = []
    standalone_short_term_borrowing = []
    standalone_cash_n_cash_eqi = []
    try:
        standAlone = getYear()
        standAloneYear_url = driver.current_url
        standAloneL.append(standAloneYear_url)
        standalone_total_shares_funds.append(
            get_table_row_data("Total Shareholders Funds"))
        standalone_long_term_borrowing.append(
            get_table_row_data("Long Term Borrowings"))
        standalone_short_term_borrowing.append(
            get_table_row_data("Short Term Borrowings"))
        standalone_cash_n_cash_eqi.append(
            get_table_row_data("Cash And Cash Equivalents"))

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
            try:
                driver.get(standAloneYear_url2)
                print("info: going to next standalone link")
            except TimeoutException as e:
                print("error : cant load next standalone link")
                logFile.write("\nerror : cant load next standalone link")
                print(e)
            except Exception as e:
                print("error : cant find next standalone link")
                logFile.write("\nerror : cant find next standalone link")
                print(e)

            standalone_total_shares_funds.append(
                get_table_row_data("Total Shareholders Funds"))
            standalone_long_term_borrowing.append(
                get_table_row_data("Long Term Borrowings"))
            standalone_short_term_borrowing.append(
                get_table_row_data("Short Term Borrowings"))
            standalone_cash_n_cash_eqi.append(
                get_table_row_data("Cash And Cash Equivalents"))
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

        consoledated_total_shares_funds.append(
            get_table_row_data("Total Shareholders Funds"))
        consoledated_long_term_borrowing.append(
            get_table_row_data("Long Term Borrowings"))
        consoledated_short_term_borrowing.append(
            get_table_row_data("Short Term Borrowings"))
        consoledated_cash_n_cash_eqi.append(
            get_table_row_data("Cash And Cash Equivalents"))

        ConsoledatedL.append(Consoledated_url)
        try:
            # print("info : Comma one...")
            di['consoledated'] = Consoledated.text.split("'")[1]
        except Exception as e:
            di['consoledated'] = Consoledated.text.split(" ")[1]
        # print(di['consoledated'] + " and waiting")
        # time.sleep(10)
        # consoledated_url2 = driver.find_element_by_xpath("//ul[@class='pagination']/")
        try:
            consoledated_url2 = getNextPageUrl()
            ConsoledatedL.append(consoledated_url2)
            try:
                driver.get(consoledated_url2)
                print("info: going to next consoledated link")
            except TimeoutException as e:
                print("error : cant load next consoledated link")
                logFile.write("\nerror : cant load next consoledated link")
                print(e)
            except Exception as e:
                print("error : cant find next consoledated link")
                logFile.write("\nerror : cant find next consoledated link")
                print(e)

            consoledated_total_shares_funds.append(
                get_table_row_data("Total Shareholders Funds"))
            consoledated_long_term_borrowing.append(
                get_table_row_data("Long Term Borrowings"))
            consoledated_short_term_borrowing.append(
                get_table_row_data("Short Term Borrowings"))
            consoledated_cash_n_cash_eqi.append(
                get_table_row_data("Cash And Cash Equivalents"))

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
        if 'consolidated' in url:
            print("info : consolidated link")
            logFile.write("\ninfo : consolidated link")
            # for d in ConsoledatedL:
            #     li.append(d)

            consoledated_total_shares_funds = consoledated_total_shares_funds[0].extend(
                consoledated_total_shares_funds[1])
            consoledated_long_term_borrowing = consoledated_long_term_borrowing[0].extend(
                consoledated_long_term_borrowing[1])
            consoledated_short_term_borrowing = consoledated_short_term_borrowing[0].extend(
                consoledated_short_term_borrowing[1])
            consoledated_cash_n_cash_eqi = consoledated_cash_n_cash_eqi[0].extend(
                consoledated_cash_n_cash_eqi[1])

            print(consoledated_total_shares_funds)
            print(consoledated_long_term_borrowing)
            print(consoledated_short_term_borrowing)
            print(consoledated_cash_n_cash_eqi)

            li.append(consoledated_total_shares_funds)
            li.append(consoledated_long_term_borrowing)
            li.append(consoledated_short_term_borrowing)
            li.append(consoledated_cash_n_cash_eqi)
        # elif(int(di['consoledated']) < int(di['standalone'])):
        #     # print("standalone")
        #     for d in standAloneL:
        #         li.append(d)
        else:
            print("info : Standalone link")
            logFile.write("\ninfo : Standalone link")
            # for d in standAloneL:
            #     li.append(d)
            standalone_total_shares_funds = standalone_total_shares_funds[0].extend(
                standalone_total_shares_funds[1])
            standalone_long_term_borrowing = standalone_long_term_borrowing[0].extend(
                standalone_long_term_borrowing[1])
            standalone_short_term_borrowing = standalone_short_term_borrowing[0].extend(
                standalone_short_term_borrowing[1])
            standalone_cash_n_cash_eqi = standalone_cash_n_cash_eqi[0].extend(
                standalone_cash_n_cash_eqi[1])

            print(standalone_total_shares_funds)
            print(standalone_long_term_borrowing)
            print(standalone_short_term_borrowing)
            print(standalone_cash_n_cash_eqi)

            li.append(standalone_total_shares_funds)
            li.append(standalone_long_term_borrowing)
            li.append(standalone_short_term_borrowing)
            li.append(standalone_cash_n_cash_eqi)

            # for e in standalone_total_shares_funds:
            #     li.append(e)
    except Exception as e:
        # print("consoledated")
        for d in ConsoledatedL:
            li.append(d)


driver.maximize_window()
driver.set_page_load_timeout(15)
# open link
# driver.set_page_load_timeout(120)
# driver.set_page_load_timeout(30)

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
# for index in range(no_of_companies):
try:
    index = 0
    name = companyName_link[2][index]
    print(name)
    screener_url = "https://www.screener.in"
    com = companyName_link[1][index]
    screener_url = screener_url+com
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
                # for , forloop
                # continue
                pass
    except Exception as e:
        logFile.write("\n"+str(e))
        print(e)
    try:
        driver.get(
            "https://www.moneycontrol.com/india/stockpricequote/" + name[0])
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

    driver.set_page_load_timeout(50)
    try:
        print("Trying BSE of : " + name)
        logFile.write("\nTrying BSE of : " + name)
        try:
            search_inp = driver.find_element_by_id("search_str")
            search_inp.send_keys(nse)
            search_inp.send_keys(Keys.ENTER)
            proceed_btn = driver.find_element_by_id("proceed-button")
            if(proceed_btn):
                try:
                    proceed_btn.click()
                    print("success : clicked send anyway")
                    logFile.write("success : clicked send anyway")
                except Exception as e:
                    print(e)
                    logFile.write("\n"+str(e))
        except TimeoutException as e:
            print("info : website taking too long to load...stopped")
            logFile.write("\ninfo : website taking too long to load...stopped")
            pass
        except Exception as error:
            print(str(error) + " cant find: " + nse)
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
        # PagesLink.append(HomePage)

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
                DriveProcess(name, stockId)
                SpreadsheetId = CheckFileDir(name)
            else:
                logFile.write("\nfile is already there")
                print("file is already there")
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)
        Nse_string = str(nse).upper()
        # print(SpreadsheetId)
        # print(Nse_string)
        driver.implicitly_wait(15)
        # scroll down to 700px
        driver.execute_script("window.scrollTo(0, 1200);")
        time.sleep(2)

        def get_sector_pe():

            try:
                sector_pe = driver.find_element_by_xpath(
                    "//td[@class='nsesc_ttm bsesc_ttm']")

                updateSingleValue(sector_pe.text, SpreadsheetId, 'B13')
                print("info : Sector PE is available")
                logFile.write("\ninfo : Sector PE is available")
                if(sector_pe.text == "0.00" or sector_pe.text == None):
                    driver.refresh()
                    get_sector_pe()

            except Exception as e:
                print("info : Sector PE is not available")
                logFile.write("\ninfo : Sector PE is not available")
        get_sector_pe()
        try:

            beta = get_table_row_data("Beta")
            updateSingleValue(str(beta[0]), SpreadsheetId, 'B10')
            print("info : Beta is available")
            logFile.write("\ninfo : Beta is available")

        except Exception as e:

            print("info : Beta is not available or " + str(e))
            logFile.write("\ninfo : Beta is not available or " + str(e))

        try:
            updateSingleValue(Nse_string, SpreadsheetId, 'B3')
        except Exception as e:
            logFile.write("\nerror : cant update ")
            logFile.write("\n"+str(e))
            print("error : cant update ")
            print(e)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)
        balancesheet_values = []
        try:
            def findBalancesheet():
                Bs = driver.find_element_by_xpath(
                    "//a[@title='Balance Sheet']")
                Bsurl = Bs.get_attribute('href')
                driver.get(Bsurl)
                time.sleep(5)
                ConOrSta(balancesheet_values, screener_url)
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

        print(balancesheet_values)
        # try getting shareholder information

        # td = driver.find_element_by_xpath(

        # values = GetLinks(SpreadsheetId)
        # values[0][0] = HomePage

        # def populatePairValues(PairLinks, index1, index2):
        #     if(len(PairLinks) == 2):
        #         values[index1][0] = PairLinks[0]
        #         values[index2][0] = PairLinks[1]
        #     elif(len(PairLinks) == 1):
        #         values[index1][0] = PairLinks[0]
        #         values[index2][0] = None
        #     else:
        #         values[index1][0] = None
        #         values[index2][0] = None
        # try:

        #     BalanceSheetLinks = Find_links("balance", PagesLink)
        #     # populatePairValues(BalanceSheetLinks, 1, 2)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)

        # time.sleep(3)
        # try:
        #     def findProfitLoss():
        #         Pl = driver.find_element_by_xpath(
        #             "//a[@title='Profit & Loss' and @class='ProfitLoss']")
        #         PLurl = Pl.get_attribute('href')
        #         driver.get(PLurl)
        #         ConOrSta(PagesLink, screener_url)
        #         logFile.write("\nsuccess : fetched Profit and Loss")
        #         print("success : fetched Profit and Loss")
        #     findProfitLoss()
        # except Exception as e:
        #     driver.refresh()
        #     logFile.write("\nTrying again to find Profit Loss")
        #     print("Trying again to find Profit Loss")
        #     findProfitLoss()
        #     logFile.write("\nCant find profit loss or " + str(e))
        #     print("Cant find profit loss or " + str(e))
        # try:
        #     ProfitLossLinks = Find_links("profit", PagesLink)
        #     populatePairValues(ProfitLossLinks, 3, 4)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)
        # # Querterly report

        # # time.sleep(3)

        # try:
        #     def findQuarReport():
        #         Qr = driver.find_element_by_xpath(
        #             "//a[@title='Quarterly Results' and @class='QuarterlyResults']")
        #         Qrurl = Qr.get_attribute('href')
        #         driver.get(Qrurl)
        #         ConOrSta(PagesLink, screener_url)
        #         logFile.write("\nsuccess : fetched Quarterly Report")
        #         print("success : fetched Quarterly Report")
        #     findQuarReport()
        # except Exception as e:
        #     driver.refresh()
        #     logFile.write("\nTrying again to find Quarterly Report")
        #     print("Trying again to find Quarterly Report")
        #     findQuarReport()
        #     logFile.write("\nCant find Qurarterly report or " + str(e))
        #     print("Cant find Qurarterly report or " + str(e))
        # try:
        #     QuarterlyLinks = Find_links("quarterly", PagesLink)
        #     populatePairValues(QuarterlyLinks, 5, 6)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)
        # # cash flow
        # try:
        #     def findCashFlow():
        #         Cf = driver.find_element_by_xpath(
        #             "//a[@title='Cash Flows' and @class='CashFlows']")
        #         Cfurl = Cf.get_attribute('href')
        #         driver.get(Cfurl)
        #         ConOrSta(PagesLink, screener_url)
        #         logFile.write("\nsuccess : fetched Cash Flow")
        #         print("success : fetched Cash Flow")
        #     findCashFlow()
        # except Exception as e:
        #     driver.refresh()
        #     logFile.write("\nTrying again to find Cash flow")
        #     print("Trying again to find Cash flow")
        #     findCashFlow()
        #     logFile.write("\nCant find Cash flow or " + str(e))
        #     print("Cant find Cash flow or " + str(e))
        # try:
        #     CashFlowLinks = Find_links("cash", PagesLink)
        #     populatePairValues(CashFlowLinks, 7, 8)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)
        # # Capital Structure
        # # time.sleep(3)

        # try:
        #     def findCapStructure():
        #         Cs = driver.find_element_by_xpath(
        #             "//a[@title='Capital Structure' and @class='CapitalStructure']")
        #         Csurl = Cs.get_attribute('href')
        #         PagesLink.append(Csurl)
        #         logFile.write("\nsuccess : fetched Capital Structure")
        #         print("success : fetched Capital Structure")
        #     findCapStructure()
        # except Exception as e:
        #     driver.refresh()
        #     logFile.write("\nTrying again to find Capital Structure")
        #     print("Trying again to find Capital Structure")
        #     findCapStructure()
        #     logFile.write("\nCant find Capital Structure or " + str(e))
        #     print("Cant find Capital Structure or " + str(e))

        # def populateSingleValues(PairLinks, index1):
        #     if(len(PairLinks) == 1):
        #         values[index1][0] = PairLinks[0]
        #     else:
        #         values[index1][0] = None
        # try:
        #     CapitalLinks = Find_links("capital", PagesLink)
        #     populateSingleValues(CapitalLinks, 9)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)
        # # for screener
        # try:

        #     PagesLink.append(screener_url)
        #     # print(screener_url)
        # except Exception as e:
        #     screener_url = None
        #     PagesLink.append(screener_url)
        #     logFile.write("\nerror : cant get screener url or " + str(e))
        #     print("error : cant get screener url or " + str(e))
        # try:
        #     ScreenerLinks = Find_links("screener", PagesLink)
        #     populateSingleValues(ScreenerLinks, 10)
        # except Exception as e:
        #     logFile.write("\n"+str(e))
        #     print(e)
        # logFile.write(str(values))
        # print(values)
        # try:
        #     UpdateLink(SpreadsheetId, values)
        # except Exception as e:
        #     print(e)
        #     logFile.write("\n"+str(e))
        #   CF screener
        try:
            driver.get(screener_url)
            driver.find_element_by_xpath(
                "//section[@id='cash-flow']/div[2]/table/tbody/tr[2]/td[1]/button").click()
            time.sleep(5)
            cf = driver.find_element_by_xpath(
                "//section[@id='cash-flow']/div[2]/table/tbody/tr[3]").text
            cf = str(cf).split(' ')
            cf = cf[3:]
            # print(cf)
        except Exception as e:
            logFile.write("\n"+str(e))
            print(e)

        if(len(cf) >= 10):
            cf = cf[-10:]
        else:
            len_cf = len(cf)
            remaining = 10-len_cf
            d_list = [' ']*remaining
            for e in d_list:
                cf.insert(0, e)
        cf_format = []
        cf_format.append(cf)
        # print(cf_format)
        try:
            UpdateCF(SpreadsheetId, cf_format)
        except Exception as e:
            print(e)
            logFile.write("\n"+str(e))

    except Exception as e:
        logFile.write("\nSomething went wrong " + str(e))
        print("Something went wrong " + str(e))
    # print(PagesLink)
except Exception as e:
    logFile.write("\n"+str(e))
    print(e)


logFile.write("\nsuccess : complete")
print("success : complete")

logFile.close()
