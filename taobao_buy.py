#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import logging
import os
import sys
from datetime import date, datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pause
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(os.getcwd() + os.sep + "log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://login.taobao.com/')

class taobao_buy:
    def __init__(self, config , click_list):
        self.clock = config['clock']
        self.cookie_path = config['cookie_path']
        
        print('CLOCK : ', self.clock)
        if self.cookie_path == "": #if none -> in the same path
            self.cookie_path = 'tb_cookies.txt'
        print('COOKIE : ', self.cookie_path)

    def login(self, browser):
        with open(self.cookie_path, 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # add cookie to browser
        for cookie in listCookies:
            cookie_dict = {
                'domain': 'taobao.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            browser.add_cookie(cookie_dict)
        sleep(10)#You can modify this waiting time
        browser.refresh()  # fresh to validate cookie
    
    def cart(self, browser):
        browser.get('https://cart.taobao.com/')
        sleep(3)
        # get multiple window
        windows = browser.window_handles
        # switch to new DM window
        browser.switch_to.window(windows[-1]) 
        print(browser.current_url) 

    def select(self, browser, click_list):
        button = browser.find_element(By.XPATH, '//*[@id="J_SelectAll1"]/div/label')
        browser.execute_script("arguments[0].click();", button)
        #todo 单独购买按钮覆盖太多层找不到了
        '''
        for click_box in click_list:
            #//*[@id="J_Order_s_3249253975_1"]/div[1]/div/div
            button = browser.find_element(By.XPATH, click_box)
            browser.execute_script("arguments[0].click();", button)
            sleep(2)
            print('click : ',click_box)
        '''
        sleep(2)
        #todo 匿名购买按钮有问题，覆盖很多层了
        #any_buy = browser.find_element(By.XPATH,'//*[@id="anonymousPC_1"]')
        #browser.execute_script("arguments[0].click();", any_buy) 
        #sleep(2)
    
    def buy(self,browser):
        checkout = browser.find_element(By.XPATH, '//*[@id="J_Go"]')
        browser.execute_script("arguments[0].click();", checkout)
        while browser.current_url == 'https://cart.taobao.com/':
            sleep(0.1)
            #sleep(10)
            # get multiple window
            windows = browser.window_handles
            # switch to new DM window
            browser.switch_to.window(windows[-1]) 
            #
        #print(browser.current_url)
        browser.find_element(By.XPATH,'//*[@id="submitOrderPC_1"]/div/a[2]').click()
        #pass

    def start(self, browser, click_list):
        try:
            if '~' in self.clock:
                set_time = self.clock
                auto_time = set_time #'2012-05-29 19~30'
                auto_time += '~00.000000'
            else: #don't set minute or hour -> 10 seconds after run the program
                logger.warn('You have not set the time!\nProgram will run after 10s for test')
                now_time = datetime.now() #.strftime('%H:%M:%S')
                set_time = now_time + timedelta(seconds=10)
                set_time = set_time.strftime("%Y-%m-%d %H~%M~%S")#string
                auto_time = set_time #'2012-05-29 19:30:03'
                auto_time += '.000000'
            sleep(2)
            self.login(browser)
            self.cart(browser)
            self.select(browser, click_list)

            #//*[@id="J_SelectAll1"]    全选
            #//*[@id="J_SelectAll1"]/div 全选的小方框
            #店铺1全部
            #/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div
            #//*[@id="J_Order_s_店铺id_1"]/div[1]/div/div 店铺1全部
            #//*[@id="J_Order_s_店铺id_1"]/div[1]/div/div
            #店铺1商品1
            #/html/body/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[1]/div/div/div

            
            auto_time = datetime.strptime(auto_time, "%Y-%m-%d %H~%M~%S.%f")
            print(auto_time)
            #2023-02-11 15:10.000000
            pause.until(auto_time)

            #todo 立刻购买
            self.buy(browser)
            now_time = datetime.now()
            print(now_time)

        except Exception as e:
            logger.exception(e)

def _get_config():
    """get json"""
    config_path = os.getcwd() + os.sep + 'TaobaoAutoBuy' + os.sep +'config.json'
    print(config_path)
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        logger.error(u'config.json Format Error')
        sys.exit()

def _analyze_xpath(config):
    shopID = config['shopID']
    click_list = []
    for shopid in shopID:
        str_item = '//*[@id="J_Order_s_'+ shopid + '_1"]/div[1]/div/div'
        click_list += [str_item]
    print(click_list)
    return click_list

if __name__ == '__main__':
    try:
        config = _get_config()
        #click_list = _analyze_xpath(config)
        tb = taobao_buy(config, click_list)
        tb.start(browser, click_list)
        logger.info('Finished\n')
    except Exception as e:
        logger.exception(e)
        logger.info('\n')
    
