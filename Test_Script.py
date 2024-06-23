#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090
#!/usr/bin/env zsh
import unittest
# Appium Python client
from appium import webdriver
from time import *
import re
import datetime
import cv2
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
wait = WebDriverWait(driver, 20)
scroll_wait = WebDriverWait(driver,10)
#opencv need
rolling ='가격순'
class TS():
    def makeTS(self):
        return str(int(datetime.datetime.now().timestamp()))


def GoHome():
    while True:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()  # 홈 탭으로 돌아가기
            break
        except:
            driver.back()

class Tests(unittest.TestCase):
    def test1(self):
        title='{타이틀명}'

        num = '{No.}'
        for loop_count in range(0, 2):
            try:
                sleep(3)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="{텍스트명}"]'))).click()
                sleep(3)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"{텍스트명}")]'))).click()
                sleep(3)
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"{텍스트명}")]')))
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"{텍스트명}")]'))).click()
                except:
                    pass
                wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("{텍스트명}")
                sleep(4)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"{텍스트명}")]'))).click()
                sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"{텍스트명}")]')))
                sleep(3)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.o_rolling + '"]')))
                sleep(10)
                amount = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"원")]'))).get_attribute("text")  # 차량 금액
                print('노출 금액 : ',  amount)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="차량 이미지는 이해를 돕기 위한 예시로, 배차 차량과 다를 수 있습니다."]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="필독사항"]')))
                Module.while_loop(self, '//*[@text="확정 확인 필요 : 영업일 기준 48시간 내에 확정"]', driver, scroll_wait, 'down_find', 1800)
                # 추가 옵션 : 노출 여부만 확인 가능(최대한 공통 요소를 선별)
                Module.while_loop(self, '//*[@text="추가 옵션 정보"]', driver, scroll_wait, 'down_find', 1500)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"렌트카 업체에서 제공 가능한 옵션입니다.")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"내비게이션")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"무료")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"겨울장비")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"가격 추후 안내")]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약하기")]'))).click()
                sleep(3)
                # 결제정보-------------------------------------------------------------------------------------------------
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="신분증(여권)과 동일한 이름을 입력해 주세요."]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("TEST")
                wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[2]'))).send_keys("CARMORE")
                # 추가 옵션 : 노출 여부만 확인 가능(최대한 공통 요소를 선별)
                Module.while_loop(self, '//*[contains(@text,"추가옵션(선택사항)")]', driver, scroll_wait, 'down_click', 1600)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"추가 옵션은 예약과 함께 해당 렌트카 업체에 요청됩니다.")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"차일드 카시트")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"JPY")]')))
                # wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[11]'))).click()  # 첫번째 옵션 선택 #요소가 불안정하여 사용 불가
                optionamount = wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView[contains(@text,"약 ")])[3]'))).get_attribute("text")
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
                # print("옵션가 :", optionamount)
                # # 총 금액 변동₩
                # amount = int(re.sub(r"[^0-9]", "", amount))
                # optionamount = int(re.sub(r"[^0-9]", "", optionamount))
                # total = amount + optionamount
                # total = str(format(total, ','))
                # print("차량 금액 + 옵션 금액 = 총금액 :", total)
                # wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + total + '")]')))
                # 결제 정보
                Module.while_loop(self, '//*[contains(@text,"결제 정보")]', driver, scroll_wait, 'down_find', 1800)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"일부 현장 결제")]')))
                # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"추가 옵션 요금")]')))
                # 대여규정
                Module.while_loop(self, '//*[contains(@text,"대여규정")]', driver, scroll_wait, 'down_find', 1800)
                wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="보기"])[2]'))).click()
                sleep(2)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"신분증 종류")]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"유효한 여권")]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"운전면허증")]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"실물 운전면허증+국제운전면허증")]')))
                # 취소규정
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소규정"]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="무료취소"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"취소수수료")]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="환불 불가"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"본 예약 상품 및 상세 내용은 토요타")]')))
                driver.back()
                sleep(2)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약하기")]'))).click()
                sleep(3)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
                # 탑승 인원 수 선택
                Module.while_loop(self, '//*[contains(@text,"인원수 선택")]', driver, scroll_wait, 'down_click', 2000)
                sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="2"]'))).click()
                sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="2"]')))  # 인원 수 선택 완료 확인
                Module.TossPay('o_short_api', 'carmore', driver, wait)
                driver.back()
                driver.back()
                driver.back()
                driver.back()
                Module.while_click_back('//*[@text="홈"]', driver, wait)
            except:
                if loop_count == 1:
                    Module.Fail(title, num,'')
                    print("Fail 시점", datetime.now())
                    self.assertEqual(0, 1)
                    break
                else:
                    Module.L_exception(driver,wait)
            else:
                Module.Pass(title, num,'')
                print("Pass 시점", datetime.now())
                break


unittest.main()
