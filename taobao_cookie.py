from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

import json
if __name__ == '__main__':

  option = webdriver.ChromeOptions()
  #option.add_experimental_option("mobileEmulation", mobile_emulation)
  option.add_experimental_option('excludeSwitches', ['enable-automation'])   # developer mode
  driver = webdriver.Chrome(options=option)

  driver.maximize_window()
  driver.get('https://login.taobao.com/')
  sleep(4)
  #driver.find_element(By.XPATH,'//*[@id="pl_login_form"]/div/div[1]/div/a[2]').click()
  sleep(30)#You can modify this waiting time for login, better to use SMS
  dictCookies = driver.get_cookies() 
  jsonCookies = json.dumps(dictCookies) 
  with open('tb_cookies.txt', 'w') as f:
    f.write(jsonCookies)
  print('cookies saved!')
  driver.close()
  driver.quit()
