#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Medium Article - Line Notify + Yahoo Finance GBPUSD Price

@author: Pei Wu https://medium.com/@mysterycatt
"""
import requests
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# LINE Notify Set-up #
token = 'PUT YOUR TOKEN HERE'
headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-from-urlencoded"
        }

# Headless Chrom Driver Set-up #
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options,
                          executable_path=os.getcwd()+'/new/chromedriver')


# Connect to the page we want #
url = 'https://finance.yahoo.com/quote/GBPUSD=X?p=GBPUSD=X'
driver.get(url)
time.sleep(2)
accept_path = '//*[@id="consent-page"]/div/div/div/div[3]/div/form/button[1]'
driver.find_element_by_xpath(accept_path).click()


# Indefinite Loop for sending us price data continuously #
while True:
    # Get page content and information
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    market_time = soup.find_all('div', attrs={'id': 'quote-market-notice'})[0].text
    price = soup.find_all('span', attrs={'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})[0].text
    # Send LINE message #
    params = {"message": market_time + "Price: " + price}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
    # Stop for 60 seconds, refresh the page then continue the loop
    time.sleep(60)
    driver.refresh()
    time.sleep(1)
