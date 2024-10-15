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
import os
import getpass
username = getpass.getuser()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
#여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())
def test1():
    title='[회원] 마이페이지 설정 ~ 쿠폰/포인트'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"My")]'))).click()
        sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="마이페이지"]')))
        sleep(5)
        #설정 버튼 클릭하기
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click() #설정 버튼
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="설정"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="약관관련"]')))
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="버전 정보최신버전"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click()  # 뒤로가기 <- 버튼
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="패밀리 소개"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="카모아 패밀리 소개"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="카모아 패밀리!"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click()  # 뒤로가기 <- 버튼
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="마이페이지"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포인트")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="포인트 내역"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click()  # 뒤로가기 <- 버튼
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"쿠폰")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰함"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰 등록"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="등록"]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test2():
    title = '[회원] 패밀리 라운지 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"My")]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"예약내역")]')))
        sleep(5)
        Module.up_swipe(driver)
        Module.up_swipe(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"패밀리라운지")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="카모아 패밀리 라운지"]')))
        Module.while_loop('//*[contains(@text,"김포공항 주차장")]', driver, 'down_click', 1900)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="업체 이미지(0)"]')))  # 이게 없으면 사진이 하나도 안뜬다는 것..!
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약하고 혜택받기"]'))) #이슈 수정 전까지는 그냥 주석 처리
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test3():
    title = '[회원] 간편 카드 관리'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"My")]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"예약내역")]')))
        sleep(5)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[@text="간편 카드 관리"]', driver, 'down_click', 1800)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="간편 카드 관리"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"추가하기")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"개인")]')))
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
