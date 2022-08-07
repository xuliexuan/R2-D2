#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import akshare as ak
from pathlib import Path
import pandas

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common import userPrint

class covDataFromXinLang_api(object):
    def __init__(self):
        pass

    #*******************************************************
    #@Name: getHSRealCovData
    #@Function: Real tick data from Sina
    #*******************************************************
    def getHSRealCovData(self):
        userPrint.infoPrint("[XinLang] Get ShangHai and ShenZhen conv real data!")
        dataSrc = ak.bond_zh_hs_cov_spot()
        return dataSrc

    #*******************************************************
    #@Name: getHSHistoryDailyCovData
    #@Function: Historical daily date from Sina
    #@example:
    #@  symbol="sz128039"
    #*******************************************************
    def getHSHistoryDailyCovData(self, symbol):
        userPrint.infoPrint("[XinLang] Get ShangHai and ShenZhen conv history data!")
        dataSrc = ak.bond_zh_hs_cov_daily(symbol)
        return dataSrc

class covDataFromEast_api(object):
    def __init__(self):
        pass

    #*******************************************************
    #@Name: getHSHistoryCovData
    #@Function: Historical tick data from Eastmoney web
    #@example:
    #@  symbol="sz128039",
    #@  period="5",
    #@  adjust="",
    #@  date="20220705"
    #*******************************************************
    def getHSHistoryTickData(self, symbol, period, date="", daynum=0):
        year = date[0:4]
        mouth = date[4:6]
        day = date[6:9]

        if date == "":
            date = time.strftime('%Y-%m-%d', time.localtime())
            start_date = date + " 09:30:00"
            end_date = date + " 15:00:00"
        else:
            date = year + "-" + mouth + "-" + day
            dt = datetime.datetime.strptime(date, "%Y-%m-%d")
            out_date = (dt + datetime.timedelta(days=daynum)).strftime("%Y-%m-%d")
            start_date = date + " 09:30:00"
            end_date = out_date + " 15:00:00"


        print("start_date", start_date)
        print("end_date", end_date)

        # start_date="2022-07-05 09:30:00",
        # end_date="2022-07-05 15:00:00"
        userPrint.infoPrint("[EAST] Get ShangHai and ShenZhen conv history data!")
        dataSrc = ak.bond_zh_hs_cov_min(symbol, period, start_date=start_date, end_date=end_date)

        return dataSrc
    #*******************************************************
    #@Name: getHSCovInfor
    #@Function: ALL Conv Information from Eastmoney web
    #*******************************************************
    def getHSCovInfor(self):
        userPrint.infoPrint("[EAST] Get ShangHai and ShenZhen Conv Information!")
        convInfor = ak.bond_zh_cov()

        return convInfor

    #*******************************************************
    #@Name: getHSConvValueAnalysis
    #@Function: Get Conv Premium rate analysis from Eastmoney web
    #*******************************************************
    def getHSConvValueAnalysis(self, symbol):
        userPrint.infoPrint("[EAST] Get ShangHai and ShenZhen Conv premium rate analysis!")
        convPreRateAnalysis = ak.bond_zh_cov_value_analysis(symbol=symbol)

        return convPreRateAnalysis

    #*******************************************************
    #@Name: covDataFromJsl_api
    #@Function: Get Conv Data from JSL
    #*******************************************************
class covDataFromJsl_api(object):
    def __init__(self):
        self.tablesUrl = 'https://www.jisilu.cn/data/cbnew/#cb'
        self.excelName = 'allGslData.xlsx'
        self.allTables = []
        self.userName = "lxxuzju"
        self.userPassword = "xu1992??"
        self.userId = ""

    def searchUserId(self):
        userUrl = 'https://www.jisilu.cn/people/{}'.format(str(self.userName))
        userData = requests.get(userUrl)
        self.userId = re.findall('var PEOPLE_USER_ID = \'(\d+)\';'  , userData.text)[0]

    def login(self, browser):
        loginLab = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[4]/div/div/a[1]')
        loginLab.click()
        input_name = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[2]/input')
        input_name.send_keys(self.userName)
        password = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[3]/input')
        password.send_keys(self.userPassword)
        time.sleep(0.5)
        tick_1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[5]/div[1]/input')
        tick_1.click()
        submit = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[5]/div[2]/input')
        submit.click()
        submit = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[1]/div[3]/form/div[6]/a')
        submit.click()

    def browserOperation(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--headless") #miss open web option
        driver = webdriver.Chrome(options=options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
                """
        })
        return driver

    def getRealConvData(self):
        browser = self.browserOperation()
        browser.get(self.tablesUrl)
        self.login(browser)
        time.sleep(15)

        tablesData = browser.page_source
        self.allTables = pandas.read_html(tablesData, header=1)

        browser.quit()
        df = self.allTables[0]

        print(df)


    # def getRealConvData(self):
    #     convRealData = ak.bond_cb_jsl(cookie=self.userCookie)
    #     return convRealData

if __name__ == '__main__':
    covDataApiClass_EAST = covDataFromEast_api()
    covDataApiClass_XL = covDataFromXinLang_api()
    convDataApiClass_JSL = covDataFromJsl_api()
    # hsRealCovData = covDataApiClass_XL.getHSRealCovData()
    # print(hsRealCovData)

    # hsHistoryCovData = covDataApiClass_XL.getHSHistoryDailyCovData("sz123106")
    # print(hsHistoryCovData)

    # hsHistoryCovData = covDataApiClass_EAST.getHSHistoryTickData("sz123106", "5", date="20220225", daynum=100)
    # print(hsHistoryCovData)

    # hsConvInformation = covDataApiClass_EAST.getHSCovInfor()
    # print(hsConvInformation)

    # convPreDataAnalysis = covDataApiClass_EAST.getHSConvValueAnalysis("123106")
    # print(convPreDataAnalysis)

    convRealData = convDataApiClass_JSL.getRealConvData()
    print(convRealData)


