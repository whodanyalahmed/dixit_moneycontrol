from selenium import webdriver
import selenium
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time,sys,os
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import pandas as pd
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
print("\n\nProcessing.....")
LOGGER.setLevel(logging.WARNING)
driver =webdriver.Chrome(path)
def getYear():
    return driver.find_element_by_xpath("//div[@id='standalone-new']/div[@class='financial-table']/table[@class='mctable1']/tbody/tr[0]/td[0]")
driver.maximize_window()
# open link
# driver.set_page_load_timeout(120)
driver.set_page_load_timeout(30)

# data = pd.read_csv("Equity.csv")
# data = data['Security Id'] 
shortcode = "HDFC"
name = "HOUSING DEVELOPMENT FINANCE CORP.LTD"
try:
    driver.get("https://www.moneycontrol.com/india/stockpricequote/" + name[0])
    print("success : Loaded...")
except TimeoutException as e:
    print("info : website taking too long to load...stopped")
    # driver.refresh()


# for d in data:    
nameList = name.split(" ")
links = []

try:

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
        except Exception as e:
            print("error : cant find the link on " + tempname)
    print(links)
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
    try:
        driver.find_element_by_xpath("//a[@title='Balance Sheet']").click()
    except Exception as e:
        print("error : cant find balance sheet ")
    print("waiting")
    time.sleep(5)
    # driver.close()
    # print("changing tab")
    # driver.switch_to.window(driver.window_handles[0])
    # driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.set_script_timeout(40)
    driver.execute_script("window.scrollTo(0, 700)") 
    try:
        standAloneYear = getYear()
        standAloneYear_url = driver.current_url
        print(standAloneYear.text)

    except Exception as e:
        print("error : cant find standalone years "+str(e))
    
    # try:
    #     driver.find_element_by_id("#consolidated").click()
    # except Exception as e:
    #     print("error : cant find consoledated link "+str(e))
    
    # try:
    #     Consoledated = getYear()
    #     Consoledated_url = driver.current_url
    #     print(Consoledated.text)

    # except Exception as e:
    #     print("error : cant find standalone years "+str(e))

    # search.send_keys(Keys.CONTROL + "a")
    # search.send_keys(Keys.DELETE)
except Exception as e:
    print("Something went wrong" + str(e))


print("success : complete")