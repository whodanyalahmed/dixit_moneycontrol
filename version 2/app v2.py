import datetime
from selenium import webdriver
from screen import GatherData
from spread import getRange, updateRange, updateSingleValue, UpdateCF, UpdateLink
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
# check length of the list must be 10 if not then add dots


def checklength(li):
    if(len(li) != 10):
        for i in range(len(li), 10):
            li.append(".")
    return li


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


def get_BalanceSheet_data(li, url):
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

            consoledated_total_shares_funds_final = sum(
                consoledated_total_shares_funds, [])
            consoledated_long_term_borrowing_final = sum(
                consoledated_long_term_borrowing, [])
            consoledated_short_term_borrowing_final = sum(
                consoledated_short_term_borrowing, [])
            consoledated_cash_n_cash_eqi_final = sum(
                consoledated_cash_n_cash_eqi, [])

            print(consoledated_total_shares_funds_final)
            print(consoledated_long_term_borrowing_final)
            print(consoledated_short_term_borrowing_final)
            print(consoledated_cash_n_cash_eqi_final)

            li.append(consoledated_total_shares_funds_final)
            li.append(consoledated_long_term_borrowing_final)
            li.append(consoledated_short_term_borrowing_final)
            li.append(consoledated_cash_n_cash_eqi_final)
        # elif(int(di['consoledated']) < int(di['standalone'])):
        #     # print("standalone")
        #     for d in standAloneL:
        #         li.append(d)
        else:
            print("info : Standalone link")
            logFile.write("\ninfo : Standalone link")
            # for d in standAloneL:
            #     li.append(d)

            standalone_total_shares_funds_final = sum(
                standalone_total_shares_funds, [])
            standalone_long_term_borrowing_final = sum(
                standalone_long_term_borrowing, [])
            standalone_short_term_borrowing_final = sum(
                standalone_short_term_borrowing, [])
            standalone_cash_n_cash_eqi_final = sum(
                standalone_cash_n_cash_eqi, [])

            print(standalone_total_shares_funds_final)
            print(standalone_long_term_borrowing_final)
            print(standalone_short_term_borrowing_final)
            print(standalone_cash_n_cash_eqi_final)

            li.append(standalone_total_shares_funds_final)
            li.append(standalone_long_term_borrowing_final)
            li.append(standalone_short_term_borrowing_final)
            li.append(standalone_cash_n_cash_eqi_final)

            # for e in standalone_total_shares_funds:
            #     li.append(e)
    except Exception as e:
        # print("consoledated")
        for d in ConsoledatedL:
            li.append(d)
        consoledated_total_shares_funds_final = sum(
            consoledated_total_shares_funds, [])
        consoledated_long_term_borrowing_final = sum(
            consoledated_long_term_borrowing, [])
        consoledated_short_term_borrowing_final = sum(
            consoledated_short_term_borrowing, [])
        consoledated_cash_n_cash_eqi_final = sum(
            consoledated_cash_n_cash_eqi, [])

        print(consoledated_total_shares_funds_final)
        print(consoledated_long_term_borrowing_final)
        print(consoledated_short_term_borrowing_final)
        print(consoledated_cash_n_cash_eqi_final)

        li.append(consoledated_total_shares_funds_final)
        li.append(consoledated_long_term_borrowing_final)
        li.append(consoledated_short_term_borrowing_final)
        li.append(consoledated_cash_n_cash_eqi_final)


def get_ProfitLoss_data(li, url):
    standAloneL = []
    ConsoledatedL = []
    di = {}
    consoledated_years = []
    consoledated_rev_from_op = []
    consoledated_finance_cost = []
    consoledated_dep_and_amor_exp = []
    consoledated_PL_bef_tax = []
    consoledated_PL_for_period = []

    standalone_years = []
    standalone_rev_from_op = []
    standalone_finance_cost = []
    standalone_dep_and_amor_exp = []
    standalone_PL_bef_tax = []
    standalone_PL_for_period = []
    try:
        standAlone = getYear()
        standAloneYear_url = driver.current_url
        standAloneL.append(standAloneYear_url)
        standalone_years.append(
            get_table_row_data("Profit & Loss account of Pazel International "))
        standalone_rev_from_op.append(
            get_table_row_data("Revenue From Operations [Net]"))
        standalone_finance_cost.append(
            get_table_row_data("Finance Costs"))
        standalone_dep_and_amor_exp.append(
            get_table_row_data("Depreciation And Amortisation Expenses"))
        standalone_PL_bef_tax.append(
            get_table_row_data("Profit/Loss Before Tax"))
        standalone_PL_for_period.append(
            get_table_row_data("Profit/Loss For The Period"))

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

            standalone_years.append(
                get_table_row_data("Profit & Loss account of Pazel International "))
            standalone_rev_from_op.append(
                get_table_row_data("Revenue From Operations [Net]"))
            standalone_finance_cost.append(
                get_table_row_data("Finance Costs"))
            standalone_dep_and_amor_exp.append(
                get_table_row_data("Depreciation And Amortisation Expenses"))
            standalone_PL_bef_tax.append(
                get_table_row_data("Profit/Loss Before Tax"))
            standalone_PL_for_period.append(
                get_table_row_data("Profit/Loss For The Period"))

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

        consoledated_years.append(
            get_table_row_data("Profit & Loss account of Pazel International "))
        consoledated_rev_from_op.append(
            get_table_row_data("Revenue From Operations [Net]"))
        consoledated_finance_cost.append(
            get_table_row_data("Finance Costs"))
        consoledated_dep_and_amor_exp.append(
            get_table_row_data("Depreciation And Amortisation Expenses"))
        consoledated_PL_bef_tax.append(
            get_table_row_data("Profit/Loss Before Tax"))
        consoledated_PL_for_period.append(
            get_table_row_data("Profit/Loss For The Period"))

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

            consoledated_years.append(
                get_table_row_data("Profit & Loss account of Pazel International "))
            consoledated_rev_from_op.append(
                get_table_row_data("Revenue From Operations [Net]"))
            consoledated_finance_cost.append(
                get_table_row_data("Finance Costs"))
            consoledated_dep_and_amor_exp.append(
                get_table_row_data("Depreciation And Amortisation Expenses"))
            consoledated_PL_bef_tax.append(
                get_table_row_data("Profit/Loss Before Tax"))
            consoledated_PL_for_period.append(
                get_table_row_data("Profit/Loss For The Period"))

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
            consoledated_years_final = sum(consoledated_years, [])
            consoledated_rev_from_op_final = sum(consoledated_rev_from_op, [])
            consoledated_finance_cost_final = sum(
                consoledated_finance_cost, [])
            consoledated_dep_and_amor_exp_final = sum(
                consoledated_dep_and_amor_exp, [])
            consoledated_PL_bef_tax_final = sum(consoledated_PL_bef_tax, [])
            consoledated_PL_for_period_final = sum(
                consoledated_PL_for_period, [])

            print(consoledated_years_final)
            print(consoledated_rev_from_op_final)
            print(consoledated_finance_cost_final)
            print(consoledated_dep_and_amor_exp_final)
            print(consoledated_PL_bef_tax_final)
            print(consoledated_PL_for_period_final)

            li.append(consoledated_years_final)
            li.append(consoledated_rev_from_op_final)
            li.append(consoledated_finance_cost_final)
            li.append(consoledated_dep_and_amor_exp_final)
            li.append(consoledated_PL_bef_tax_final)
            li.append(consoledated_PL_for_period_final)

        # elif(int(di['consoledated']) < int(di['standalone'])):
        #     # print("standalone")
        #     for d in standAloneL:
        #         li.append(d)
        else:
            print("info : Standalone link")
            logFile.write("\ninfo : Standalone link")
            # for d in standAloneL:
            #     li.append(d)

            standalone_years_final = sum(standalone_years, [])
            standalone_rev_from_op_final = sum(standalone_rev_from_op, [])
            standalone_finance_cost_final = sum(standalone_finance_cost, [])
            standalone_dep_and_amor_exp_final = sum(
                standalone_dep_and_amor_exp, [])
            standalone_PL_bef_tax_final = sum(standalone_PL_bef_tax, [])
            standalone_PL_for_period_final = sum(standalone_PL_for_period, [])

            print(standalone_years_final)
            print(standalone_rev_from_op_final)
            print(standalone_finance_cost_final)
            print(standalone_dep_and_amor_exp_final)
            print(standalone_PL_bef_tax_final)
            print(standalone_PL_for_period_final)

            li.append(standalone_years_final)
            li.append(standalone_rev_from_op_final)
            li.append(standalone_finance_cost_final)
            li.append(standalone_dep_and_amor_exp_final)
            li.append(standalone_PL_bef_tax_final)
            li.append(standalone_PL_for_period_final)

            # for e in standalone_total_shares_funds:
            #     li.append(e)
    except Exception as e:
        # print("consoledated")
        for d in ConsoledatedL:
            li.append(d)
            consoledated_years_final = sum(consoledated_years, [])
            consoledated_rev_from_op_final = sum(consoledated_rev_from_op, [])
            consoledated_finance_cost_final = sum(
                consoledated_finance_cost, [])
            consoledated_dep_and_amor_exp_final = sum(
                consoledated_dep_and_amor_exp, [])
            consoledated_PL_bef_tax_final = sum(consoledated_PL_bef_tax, [])
            consoledated_PL_for_period_final = sum(
                consoledated_PL_for_period, [])

            print(consoledated_years_final)
            print(consoledated_rev_from_op_final)
            print(consoledated_finance_cost_final)
            print(consoledated_dep_and_amor_exp_final)
            print(consoledated_PL_bef_tax_final)
            print(consoledated_PL_for_period_final)

            li.append(consoledated_years_final)
            li.append(consoledated_rev_from_op_final)
            li.append(consoledated_finance_cost_final)
            li.append(consoledated_dep_and_amor_exp_final)
            li.append(consoledated_PL_bef_tax_final)
            li.append(consoledated_PL_for_period_final)


def get_Quarterly_data(li, url):
    standAloneL = []
    ConsoledatedL = []
    di = {}
    consoledated_net_SI_from_profit = []
    consoledated_net_PL_for_period = []
    consoledated_before_other_item_tax = []

    standalone_net_SI_from_profit = []
    standalone_net_PL_for_period = []
    standalone_before_other_item_tax = []
    try:
        standAlone = getYear()
        standAloneYear_url = driver.current_url
        standAloneL.append(standAloneYear_url)
        standalone_net_SI_from_profit.append(
            get_table_row_data("Net Sales/Income from operations"))
        standalone_net_PL_for_period.append(
            get_table_row_data("Net Profit/(Loss) For the Period"))
        standalone_before_other_item_tax.append(
            get_table_row_data("P/L Before Other Inc. , Int., Excpt. Items & Tax"))

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

            standalone_net_SI_from_profit.append(
                get_table_row_data("Net Sales/Income from operations"))
            standalone_net_PL_for_period.append(
                get_table_row_data("Net Profit/(Loss) For the Period"))
            standalone_before_other_item_tax.append(
                get_table_row_data("P/L Before Other Inc. , Int., Excpt. Items & Tax"))

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

        consoledated_net_SI_from_profit.append(
            get_table_row_data("Net Sales/Income from operations"))
        consoledated_net_PL_for_period.append(
            get_table_row_data("Net Profit/(Loss) For the Period"))
        consoledated_before_other_item_tax.append(
            get_table_row_data("P/L Before Other Inc. , Int., Excpt. Items & Tax"))

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
            consoledated_net_SI_from_profit.append(
                get_table_row_data("Net Sales/Income from operations"))
            consoledated_net_PL_for_period.append(
                get_table_row_data("Net Profit/(Loss) For the Period"))
            consoledated_before_other_item_tax.append(
                get_table_row_data("P/L Before Other Inc. , Int., Excpt. Items & Tax"))

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

            consoledated_net_SI_from_profit_final = sum(
                consoledated_net_SI_from_profit, [])
            consoledated_net_PL_for_period_final = sum(
                consoledated_net_PL_for_period, [])
            consoledated_before_other_item_tax_final = sum(
                consoledated_before_other_item_tax, [])

            print(consoledated_net_SI_from_profit_final)
            print(consoledated_net_PL_for_period_final)
            print(consoledated_before_other_item_tax_final)

            li.append(consoledated_net_SI_from_profit_final)
            li.append(consoledated_net_PL_for_period_final)
            li.append(consoledated_before_other_item_tax_final)
        # elif(int(di['consoledated']) < int(di['standalone'])):
        #     # print("standalone")
        #     for d in standAloneL:
        #         li.append(d)
        else:
            print("info : Standalone link")
            logFile.write("\ninfo : Standalone link")
            # for d in standAloneL:
            #     li.append(d)

            standalone_net_SI_from_profit_final = sum(
                standalone_net_SI_from_profit, [])
            standalone_net_PL_for_period_final = sum(
                standalone_net_PL_for_period, [])
            standalone_before_other_item_tax_final = sum(
                standalone_before_other_item_tax, [])

            print(standalone_net_SI_from_profit_final)
            print(standalone_net_PL_for_period_final)
            print(standalone_before_other_item_tax_final)

            li.append(standalone_net_SI_from_profit_final)
            li.append(standalone_net_PL_for_period_final)
            li.append(standalone_before_other_item_tax_final)

            # for e in standalone_total_shares_funds:
            #     li.append(e)
    except Exception as e:
        # print("consoledated")
        for d in ConsoledatedL:
            li.append(d)

        consoledated_net_SI_from_profit_final = sum(
            consoledated_net_SI_from_profit, [])
        consoledated_net_PL_for_period_final = sum(
            consoledated_net_PL_for_period, [])
        consoledated_before_other_item_tax_final = sum(
            consoledated_before_other_item_tax, [])

        print(consoledated_net_SI_from_profit_final)
        print(consoledated_net_PL_for_period_final)
        print(consoledated_before_other_item_tax_final)

        li.append(consoledated_net_SI_from_profit_final)
        li.append(consoledated_net_PL_for_period_final)
        li.append(consoledated_before_other_item_tax_final)


def get_CashFlow_data(li, url):
    standAloneL = []
    ConsoledatedL = []
    di = {}
    consoledated_net_cash_from_OA = []

    standalone_net_cash_from_OA = []
    try:
        standAlone = getYear()
        standAloneYear_url = driver.current_url
        standAloneL.append(standAloneYear_url)
        standalone_net_cash_from_OA.append(
            get_table_row_data("Net CashFlow From Operating Activities"))

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

            standalone_net_cash_from_OA.append(
                get_table_row_data("Net CashFlow From Operating Activities"))

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

        consoledated_net_cash_from_OA.append(
            get_table_row_data("Net CashFlow From Operating Activities"))

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
            consoledated_net_cash_from_OA.append(
                get_table_row_data("Net CashFlow From Operating Activities"))

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

            consoledated_net_cash_from_OA_final = sum(
                consoledated_net_cash_from_OA, [])
            print(consoledated_net_cash_from_OA_final)

            li.append(consoledated_net_cash_from_OA_final)

        # elif(int(di['consoledated']) < int(di['standalone'])):
        #     # print("standalone")
        #     for d in standAloneL:
        #         li.append(d)
        else:
            print("info : Standalone link")
            logFile.write("\ninfo : Standalone link")
            # for d in standAloneL:
            #     li.append(d)

            standalone_net_cash_from_OA_final = sum(
                standalone_net_cash_from_OA, [])

            print(standalone_net_cash_from_OA_final)
            li.append(standalone_net_cash_from_OA_final)

            # for e in standalone_total_shares_funds:
            #     li.append(e)
    except Exception as e:
        # print("consoledated")
        for d in ConsoledatedL:
            li.append(d)

        consoledated_net_cash_from_OA_final = sum(
            consoledated_net_cash_from_OA, [])
        print(consoledated_net_cash_from_OA_final)

        li.append(consoledated_net_cash_from_OA_final)


def get_capital_structure_data(table_data):
    driver.implicitly_wait(10)
    try:
        # get all the table rows with class mctable1 and store in a list
        table_rows = driver.find_elements_by_xpath(
            "//table[@class='mctable1']/tbody/tr")

        for table_row in table_rows:
            # get table_row td values
            try:
                temp = []
                table_row_td = table_row.find_elements_by_tag_name("td")

                counter = 0
                for data in table_row_td:
                    if(counter == 0 or counter == 4 or counter == 5):
                        if (counter == 0):
                            years = data.find_elements_by_tag_name("span")
                            temp.append(years[0].text+" to " + years[1].text)
                        else:
                            temp.append(data.text)

                    # print(data)
                    counter += 1
                table_data.append(temp)
            except Exception as e:
                print("error: table row not found")
                print(e)
        print(table_data)
        print("info: with these "+str(len(table_data))+" number of data")
        if(len(table_data) > 10):
            # get first 10 elements and save in same list
            print("info: Data is more then 10 years trimming it to 10 years")
            table_data = table_data[0:10]
        print(table_data)
        print("info: with these "+str(len(table_data))+" number of data")
    except Exception as e:
        print("error: table not loaded")
        print(e)


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
for index in range(no_of_companies):
    try:
        # index = 0
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
                    print("info : skipping element already there")
                    # for , forloop
                    continue
                    # pass
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
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
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

            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
            driver.implicitly_wait(15)
            balancesheet_values = []
            try:
                def findBalancesheet():
                    Bs = driver.find_element_by_xpath(
                        "//a[@title='Balance Sheet']")
                    Bsurl = Bs.get_attribute('href')
                    driver.get(Bsurl)
                    time.sleep(5)
                    get_BalanceSheet_data(balancesheet_values, screener_url)
                    logFile.write("\nsuccess : fetched Balance Sheet")
                    print("success : fetched Balance Sheet")
                findBalancesheet()

            except TimeoutException as e:
                print("info : website taking too long to load...stopped")
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
                pass
            except Exception as e:
                driver.refresh()
                logFile.write("\nTrying again to find Balance Sheet")
                print("Trying again to find Balance Sheet")
                findBalancesheet()
                logFile.write("\nerror : cant find balance sheet ")
                print("error : cant find balance sheet ")

            print(balancesheet_values)
            # update total shareholders data

            def update_values_with_range(balancesheet_values, range_num, step):
                # range_num = 18
                for balancesheet_value in balancesheet_values:

                    try:
                        shareholders_Data = [checklength(balancesheet_value)]
                        balance_sheet_Range = 'K' + \
                            str(range_num)+':B'+str(range_num)
                        updateRange(SpreadsheetId, shareholders_Data,
                                    balance_sheet_Range)
                        print("info: "+balance_sheet_Range+" data is updated")
                        logFile.write("\ninfo: "+balance_sheet_Range +
                                      " data is updated")
                        range_num += step
                        # updateRange(SpreadsheetId, [balancesheet_values[0]], 'K18:B18')
                    except Exception as e:
                        print("info: "+balance_sheet_Range +
                              " data is not updated")
                        logFile.write("\ninfo: "+balance_sheet_Range +
                                      " data is not updated")
                        pass
            update_values_with_range(balancesheet_values, 18, 2)
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

            driver.implicitly_wait(15)
            Profitloss_values = []
            try:
                def findProfitLoss():
                    Pl = driver.find_element_by_xpath(
                        "//a[@title='Profit & Loss' and @class='ProfitLoss']")
                    PLurl = Pl.get_attribute('href')
                    driver.get(PLurl)
                    get_ProfitLoss_data(Profitloss_values, screener_url)
                    logFile.write("\nsuccess : fetched Profit and Loss")
                    print("success : fetched Profit and Loss")
                findProfitLoss()
            except TimeoutException as e:
                print("info : website taking too long to load...stopped")
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
                pass
            except Exception as e:
                driver.refresh()
                logFile.write("\nTrying again to find Profit Loss")
                print("Trying again to find Profit Loss")
                findProfitLoss()
                logFile.write("\nCant find profit loss or " + str(e))
                print("Cant find profit loss or " + str(e))

            print(Profitloss_values)
            update_values_with_range(Profitloss_values, 29, 2)
            # # Querterly report
            driver.implicitly_wait(10)
            Quarterly_values = []
            try:
                def findQuarReport():
                    Qr = driver.find_element_by_xpath(
                        "//a[@title='Quarterly Results' and @class='QuarterlyResults']")
                    Qrurl = Qr.get_attribute('href')
                    driver.get(Qrurl)
                    get_Quarterly_data(Quarterly_values, screener_url)
                    logFile.write("\nsuccess : fetched Quarterly Report")
                    print("success : fetched Quarterly Report")
                findQuarReport()
            except TimeoutException as e:
                print("info : website taking too long to load...stopped")
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
                pass
            except Exception as e:
                driver.refresh()
                logFile.write("\nTrying again to find Quarterly Report")
                print("Trying again to find Quarterly Report")
                findQuarReport()
                logFile.write("\nCant find Qurarterly report or " + str(e))
                print("Cant find Qurarterly report or " + str(e))

            update_values_with_range(Quarterly_values, 44, 2)
            # cash flow
            driver.implicitly_wait(10)
            CashFlow_Values = []
            try:
                def findCashFlow():
                    Cf = driver.find_element_by_xpath(
                        "//a[@title='Cash Flows' and @class='CashFlows']")
                    Cfurl = Cf.get_attribute('href')
                    driver.get(Cfurl)
                    get_CashFlow_data(CashFlow_Values, screener_url)
                    logFile.write("\nsuccess : fetched Cash Flow")
                    print("success : fetched Cash Flow")
                findCashFlow()
            except TimeoutException as e:
                print("info : website taking too long to load...stopped")
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
                pass
            except Exception as e:
                driver.refresh()
                logFile.write("\nTrying again to find Cash flow")
                print("Trying again to find Cash flow")
                findCashFlow()
                logFile.write("\nCant find Cash flow or " + str(e))
                print("Cant find Cash flow or " + str(e))

            update_values_with_range(CashFlow_Values, 54, 2)
            # try:
            #     CashFlowLinks = Find_links("cash", PagesLink)
            #     populatePairValues(CashFlowLinks, 7, 8)
            # except Exception as e:
            #     logFile.write("\n"+str(e))
            #     print(e)
            # # Capital Structure
            # # time.sleep(3)
            Capital_Structure_Data = []
            try:
                def findCapStructure():
                    Cs = driver.find_element_by_xpath(
                        "//a[@title='Capital Structure' and @class='CapitalStructure']")
                    Csurl = Cs.get_attribute('href')
                    driver.get(Csurl)
                    get_capital_structure_data(Capital_Structure_Data)
                    logFile.write("\nsuccess : fetched Capital Structure")
                    print("success : fetched Capital Structure")
                findCapStructure()

            except TimeoutException as e:
                print("info : website taking too long to load...stopped")
                logFile.write(
                    "\ninfo : website taking too long to load...stopped")
                pass
            except Exception as e:
                driver.refresh()
                logFile.write("\nTrying again to find Capital Structure")
                print("Trying again to find Capital Structure")
                findCapStructure()
                logFile.write("\nCant find Capital Structure or " + str(e))
                print("Cant find Capital Structure or " + str(e))

            range_num = 61
            step = 1
            print(getRange(SpreadsheetId, "A61:C61"))
            for balancesheet_value in Capital_Structure_Data:

                try:
                    balance_sheet_Range = 'C' + \
                        str(range_num)+':A'+str(range_num)
                    print("info : updating this value: " +
                          str([balancesheet_value]))
                    updateRange(SpreadsheetId, [balancesheet_value],
                                balance_sheet_Range)
                    print("info: "+balance_sheet_Range+" data is updated")
                    logFile.write("\ninfo: "+balance_sheet_Range +
                                  " data is updated")
                    range_num += step
                    # updateRange(SpreadsheetId, [balancesheet_values[0]], 'K18:B18')
                except Exception as e:
                    print("info: "+balance_sheet_Range+" data is not updated")
                    logFile.write("\ninfo: "+balance_sheet_Range +
                                  " data is not updated")
                    pass
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
