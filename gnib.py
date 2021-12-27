import time
from function import *
# import pygame
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pytesser3
import os
# import ctypes
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ops = Options()
ops.add_argument('--proxy-server=http://%s' % '127.0.0.1:7890')        #need to set a proxy if you are in china
ops.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
# options = webdriver.ChromeOptions().add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(executable_path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe',chrome_options=ops)
driver.get('https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm')

# pygame.mixer.init()
# track = pygame.mixer.music.load(r"./1.mp3")

### need to configure your own message service if you have
client = AcsClient('xxxxxxxx','xxxxxxxxxxx', 'xxxxxxxxxxxxxxx')
def msm(number):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "xxxxx")
    request.add_query_param('PhoneNumbers',xxxxxx)
    request.add_query_param('SignName', "xxxxxx")
    request.add_query_param('TemplateCode', "xxxxxx")
    request.add_query_param('TemplateParam', "xxxxxxxxx")
    response=client.do_action(request)
    return str(response, encoding='utf-8')

r = 1            #record refresh times
t = 1            #record search times
switch = 1 
'''
first click button of accept all in the page, or when refreshing page cookies setting will influence our program 
'''
while True:
  try:
    time.sleep(3)
    if switch:
      Select(driver.find_element(*((By.XPATH, '//select[@name="Category"]')))).select_by_value("All")      #Category
      Select(driver.find_element(*((By.XPATH, '//select[@name="SubCategory"]')))).select_by_value("All")   #Sub Category
      driver.execute_script("$(arguments[0]).click()",driver.find_element_by_xpath('//input[@name="UsrDeclaration"]'))  #Confirm
      s = Select(driver.find_element(*((By.XPATH, '//select[@name="Salutation"]')))).select_by_index("3")  ###Sex
      driver.find_element_by_xpath('//input[@name="GivenName"]').send_keys('your givenname')  #GivenName
      driver.find_element_by_xpath('//input[@name="SurName"]').send_keys('your surname')   #SurName
      ###Date of Birth###
      driver.execute_script('document.getElementById("DOB").removeAttribute("readonly")')
      driver.find_element_by_xpath('//input[@name="DOB"]').send_keys('your birthdate formed in day/month/year')
      ######
      Select(driver.find_element(*((By.XPATH, '//select[@name="Nationality"]')))).select_by_index("40")  #Nationality ,and 40 represents china
      driver.find_element_by_xpath('//input[@name="Email"]').send_keys('your email')  #Email
      driver.find_element_by_xpath('//input[@name="EmailConfirm"]').send_keys('your email')  #EmailConfirm
      Select(driver.find_element(*((By.XPATH, '//select[@name="FamAppYN"]')))).select_by_index("2")  #Family Application
      Select(driver.find_element(*((By.XPATH, '//select[@name="PPNoYN"]')))).select_by_index("1")  #Passport
      driver.find_element_by_xpath('//input[@name="PPNo"]').send_keys('your passport number')  #Passport Number
      driver.find_element_by_xpath('//button[@id="btLook4App"]').click()  # Look For Appointment
      s = Select(driver.find_element(*((By.XPATH, '//select[@name="AppSelectChoice"]')))).select_by_index("2")  #Search for appointments by:
  ######
    driver.execute_script("$(arguments[0]).click()",driver.find_element_by_xpath('//button[@id="btSrch4Apps"]'))
    print(f'-----------------------------------\nCurrent refresh times: {r-1}\nSearch: {t} times',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(15)
    picture_url = driver.save_screenshot('./screen.png')
    ### OCR ###
    # try:
    content = pytesser3.image_file_to_string('./screen.png')
    # except Exception as e:
    #   os.remove('./screen.png')
    #   time.sleep(20)
    #   picture_url = driver.save_screenshot('./screen.png')
    #   content = pytesser3.image_file_to_string('./screen.png')
    if compare_image_with_hash('./screen.png','./test.png'):
      driver.refresh()
      print(f'\n\n-------------------------------------Refresh :{r} times---------------------------------------\n\n')
      r += 1
      switch = 1
      os.remove('./screen.png')
      continue
    elif 'Please try reloading this page.' in content:
      driver.refresh()
      print(f'\n\n-------------------------------------Refresh :{r} times---------------------------------------\n\n')
      r += 1
      switch = 1
      os.remove('./screen.png')
      continue
    elif not 'No appointment(s) are currently available' in content:
      print(msm('your phone number'))
      # pygame.mixer.music.play()
      # time.sleep(180)
      # ctypes.windll.user32.MessageBoxA(0,'message','tips',0)
      break
    os.remove('./screen.png')
    switch = 0
    t += 1
  except Exception as e:
    driver.refresh()
    print(f'\n\n-------------------------------------Refresh :{r} times---------------------------------------\n\n')
    r += 1
    switch = 1

######
while True:
  time.sleep(100)

