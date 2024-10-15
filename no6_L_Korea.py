#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090
#!/usr/bin/env python3
#!/usr/bin/env bash
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
# Open iOS simulator 11.2 and install TestApp
import Module_Script
import getpass
import Module
username = getpass.getuser()
now = datetime.now()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
#여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())

def test1():
    title='[회원] 제주 1일 차량 리스트 ~ 최근 본 상품 ~ 결제 정보 (카카오페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        Module_Script.L_Jeju_RentList(wait,'no',driver)
        sleep(2)
        Module.KakaoPay('jeju','carmore',driver,wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test2():
    title = '[회원] 차량 리스트 내륙 1일 차량 상세 ~ 결제 정보 (토스페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_City_RentList(wait,driver,'carmore')
        Module.TossPay('k_short','carmore',driver,wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())



def test3():
    title = '[회원] 차량 리스트 배달가능 1일 차량 상세 ~ 결제 정보 (일반결제_NH결제)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"홈")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"계신 그곳으로")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="배달 위치 선택"]')))
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"여기서")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"검색 조건 설정")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"쓰리엠타워")]'))) #기본 지역으로 검증
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"실시간 최저가 차량 검색")]'))).click()
        sleep(5)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"집 앞까지")]'))) #파란색 차량 배달 띠
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"배달비")])[1]'))).click() #차량 선택
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"배달비")]')))
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"렌트카")]'))).click()
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"예약하기")]'))).click()
        sleep(5)
        # 결제정보
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이름"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("팀오투테스트")
        Module.NormalPay('k_short', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())



def test4():
    title = '[회원] 내륙 월렌트 3개월 depth1~결제정보 (간편카드결제 - 일시불만 노출) '
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        Module_Script.L_Month_RentList(wait, driver, 3,'carmore')
        Module.SimpleCardPay('month', 'carmore', wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="일시불"]'))).click()
        #할부 여부 확인
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"일시불")]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

if __name__ == '__main__':
    # test1()
    test2()
    # test3()
    test4()
