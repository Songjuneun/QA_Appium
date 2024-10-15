#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090

#!/usr/bin/env zsh

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
import Module
# Open iOS simulator 11.2 and install TestApp
now = datetime.now()
import os
import getpass
username = getpass.getuser()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('tmap'))
#여러줄 주석 : command + /
wait = WebDriverWait(driver,Module.wait_sec())


def test1():

    title = '[티맵 렌터카] 메인홈 패밀리 라운지 버튼 미 노출 확인'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.tmapOpen(driver, wait)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="tmap logo"]')))  # TMAP 렌터카인지 확인
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"친구초대")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"단기렌트")]')))
            try:
                # 이벤트 팝업 노출 시
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"패밀리 라운지")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"티맵 렌터카에서 패밀리 라운지가 노출 됩니다.")]')))
                break
            except:
                pass
            try:
                # 이벤트 팝업 노출 시
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"렌트카와 결합할인")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"티맵 렌터카에서 패키지가 노출 됩니다.")]')))
                break
            except:
                pass
            try:
                # 이벤트 팝업 노출 시
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"Foreigner")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"티맵 렌터카에서 Foreigner가 노출 됩니다.")]')))
                break
            except:
                pass
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break

def test2():
    title = '[티맵 렌터카] 제주 차량 리스트 ~ 최근 본 상품 ~ 결제 정보 (네이버 페이)'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.tmapOpen(driver, wait)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="tmap logo"]'))) #TMAP 렌터카인지 확인
            Module_Script.L_Jeju_RentList(wait,'tmap',driver)
            Module.NaverPay('jeju', 'tmap', driver, wait)
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break

def test3():
    title = '[티맵 렌터카] 해외 시실리 API 차량 리스트 ~ 결제 정보 (카카오페이)'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.tmapOpen(driver, wait)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"홈")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="tmap logo"]')))  # TMAP 렌터카인지 확인
            Module_Script.L_Overseas_RentList(wait,driver,'tmap','sicily')
            Module.KakaoPay('o_short_api', 'tmap', driver, wait)
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break



def test4():
    title = '[티맵 렌터카] 내륙 월렌트 depth1 ~ 결제정보 (신용.체크카드)'
    num = 'TC'
    for loop_count in range(0, 3):
        try:
            Module.tmapOpen(driver, wait)
            Module_Script.L_Month_RentList(wait, driver, 1,'tmap')
            Module.NormalPay('month', 'tmap', driver, wait)
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break


def test5():
    title = '[티맵 렌터카] 마이 탭 패밀리 혜택 미 노출, 친구 초대 미 노출 확인 하기 '
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.tmapOpen(driver, wait)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="My"]'))).click()
            sleep(3)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="마이페이지"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="나의리뷰"]')))
            # 설정 버튼 클릭하기
            wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[3]'))).click()  # 설정 버튼
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="설정"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="약관관련"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마케팅 정보 수신 동의 설정"]')))
            driver.back()
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="마이페이지"]')))
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="패밀리 소개"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="티맵 렌터카에 패밀리 소개가 노출 됩니다."]')))
                break
            except:
                pass
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포인트")]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="포인트 내역"]')))
            driver.back()
            sleep(5)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="마이페이지"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"쿠폰")]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰함"]'))) #마이그레이션 작업 후 쿠폰함 페이지로 변동
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰 등록"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="등록"]')))

        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break

def test6(): #카드가 미 노출 되는 이슈 발생 스크립트 추가
    title = '[티맵 렌터카] 마이페이지 간편 카드 관리'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.tmapOpen(driver, wait)
            sleep(3)
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"마이페이지")]')))
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"My")]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"마이페이지")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"예약내역")]')))
            sleep(5)
            Module.down_swipe(driver)
            Module.down_swipe(driver)
            Module.while_loop('//*[@text="간편 카드 관리"]', driver, 'down_click', 1800)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="간편 카드 관리"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"추가하기")]')))
            if Module.username == 'joy':
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"NH")]'))) #티맵 이슈 해결되면 법인카드 등록 필요
            else:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"신한카드신용")]')))
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
