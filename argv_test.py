#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090
#!/usr/bin/env zsh
import unittest
# Appium Python client
from appium import webdriver
from time import *
import os
import datetime
import re
import numpy as np
from datetime import *
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import Module
# Open iOS simulator 11.2 and install TestApp
now = datetime.now()
import sys
import getpass
username = getpass.getuser()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
#여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())
scroll_wait = WebDriverWait(driver,10)
#opencv need
class TS():
    def makeTS(self):
        return str(int(datetime.datetime.now().timestamp()))

def test1():
    title = '[회원] 마이페이지 설정 ~ 쿠폰/포인트'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.test_carmoreOpen(driver, wait)
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"My2")]'))).click()
        except:
            if loop_count == 1:
                Module.Fail(title, num, '', driver)
                print("Fail 시점", datetime.now())
                break
        else:
            Module.Pass(title, num, '')
            print("Pass 시점", datetime.now())
            break

if __name__ == '__main__':
    test1()

