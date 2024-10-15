#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090
#!/usr/bin/env zsh
import unittest
# Appium Python client
from appium import webdriver
from time import *
import Module_Script
import datetime
import numpy as np
from datetime import *
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
# Open iOS simulator 11.2 and install TestApp
import os
import getpass
import Module
username = getpass.getuser()
now = datetime.now()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
#여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())
def test1():
    title='[회원] 해외렌트 직판 차량 리스트_해외 필터, 차량 상세 ,결제 정보 (네이버페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_Overseas_RentList(wait,driver,'no','direct')
        sleep(3)
        Module.NaverPay('o_short_direct', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test2():
    title='[회원] 일본 히카리 API 온라인 결제 홈 컨트롤러 ~ 결제 정보 (토스페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_Overseas_RentList(wait,driver,'no','hikari')
        Module.TossPay('o_short_api', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test3():
    title='[회원] 해외 API 홈 컨트롤러 ~ 결제 정보 (카카오페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_Overseas_RentList(wait,driver,'no','api')
        Module.KakaoPay('o_short_api', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test4():
    title='[회원] 해외렌트 현장결제 상품'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_Overseas_RentList(wait,driver,'no','cash')
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


if __name__ == '__main__':
    test1()
    test2()
    test3()
    if Module.argv() != 'dev':
        test4()
    else:
        pass
