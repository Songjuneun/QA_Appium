# 테스트 수행 시간 : 2분 30초 (2023/2/15)

import unittest
# Appium Python client
from appium import webdriver
from time import *
import Module_Script
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
import Module
now = datetime.now()
# Connect to Appium server on local host
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
# 여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())
def test1():
    title='[비 회원] 호텔 > 로그인 후, 카텔 쿠폰 발급 패키지 호텔 상세 이동 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        sleep(2)
        Module_Script.hotelMore(wait,driver,'nl_ht_catel_pk','부산')
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test2():
    title = '[회원] 패키지 상품 토스페이 결제 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        sleep(2)
        Module_Script.hotelMore(wait, driver, 'l_pK','후쿠오카')
        Module.TossPay('package', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test3():
    title = '[회원] 제주 렌트카 > 슈퍼 특가 > 패키지 (네이버페이)'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"로그인 하기")]'))).click()
            Module.login(wait)
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약내역")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"홈")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"단기렌트")]'))).click()
        # 지역 설정
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="제주국제공항"]')))
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Button)[4]'))).click()
            sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제주 제주"]'))).click()  # 지역 리스트 제주
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제주도 전체"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제주국제공항"]')))
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"렌트카")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"실시간 최저가 차량 검색")]'))).click()
        sleep(5)
        #차량리스트
        amount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[1]'))).get_attribute("text")
        amount = amount.replace('원 부터', '')  # 원 제거
        print('첫번째 차량 최저 가격 :', amount)
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"' + amount + '")])[2]'))).click()
        sleep(3)
        try:
            # 차량 상세로 바로 갈 경우
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="차량 이미지는 이해를 돕기 위한 예시로, 배차 차량과 다를 수 있습니다."]')))
        except:
            # depth2 로 갈 경우
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"포함")])[1]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="차량 이미지는 이해를 돕기 위한 예시로, 배차 차량과 다를 수 있습니다."]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"필독사항")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"렌트카만")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        sleep(5)
        shopname = wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.TextView)[21]'))).get_attribute('text')
        print('업체명 :', shopname)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔과 함께 예약 시")]'))).click() #카텔 버튼 노출 시
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔까지 함께 예약 최대 60% 할인")]'))).click() #카텔 버튼 미 노출 시
        # 패키지 리스트
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔 보러가기")]'))).click() #카텔 쿠폰 안가지고 있을 떄 팝업 뜨는거 대응
        except:
            pass
        sleep(4)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약중")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"제주국제공항")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"렌트카만 바로 예약")]')))
        Module_Script.hotelMore(wait, driver, 'l_rent_catel_pk','제주')
        Module.TossPay('package', 'carmore', driver, wait)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

if __name__ == '__main__':
    test1()
    # test2()
    test3()