#수정 시 마다 드라이브 문서 수정 필요 : https://docs.google.com/spreadsheets/d/1_viQkTyrifXAtAJEApNaSkvTAPODGe-7/edit#gid=1810128090
#!/usr/bin/env python3
#!/usr/bin/env bash
import unittest
# Appium Python client
import pyautogui
from appium import webdriver
from time import *
import sys
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
server = Module.argv()
who = 'carmore'
def test1():
    title = '[회원] 차량 리스트 내륙 1일 결제 ~ 취소 (간편카드결제)'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            print('loop_count = ',loop_count)
            Module.carmoreOpen(driver, wait)
            if loop_count == 0:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
                # 뜨면 닫고
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="닫기"]')))
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="내일 다시 볼게요!"]'))).click()
                except:
                    print("메인 팝업이 없습니다. - 진짜 없는건지 확인 필요 ")
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"모두보기")]')))
            amount = Module_Script.L_City_RentList(wait,driver,'carmore')
            sleep(2)
            ansim_amount = Module.SimpleCardPay('k_dev','carmore',wait)
            sleep(2)
            #결제완료
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제 완료"]'))) #이거 풀기
            amount = int(re.sub(r"[^0-9]", "", amount))  # 공백 없애기 작업 해주고
            print('안심플러스 금액 = ', ansim_amount)
            amount = amount + int(str(ansim_amount))
            amount = str(format(amount, ','))  # 다시 콤마 붙여주기
            print('안심플러스 추가한 금액', amount)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]'))) #여기서 부터 풀기
            flag='pay_finish'
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카모아 국내 렌트카는 예약 즉시 확정됩니다!")]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"잠깐! 호텔은 예약하셨나요?")]')))
            # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"성급")]'))) #안나올 경우도 있어서 그냥 넘기기
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
            sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="서비스 개선 설문조사"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="신혼여행"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제출하기"]'))).click()
            sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
            sleep(3)
            #마이페이지
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마이페이지"]')))
            sleep(3)
            #예약카드 불러오는게 너무 느림
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약완료"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]'))).click() #예약카드 선택
            sleep(2)
            # 예약상세정보페이지
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 완료"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이메일로 예약 내역 받기"]')))
            Module.while_loop('//*[@text="결제 정보"]', driver, 'down_find', 1800)
            Module.down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="간편카드결제"]')))
            Module.down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
            Module.down_swipe(driver)
            Module.down_swipe(driver)
            Module.down_swipe(driver)
            Module.cancel_Process(wait,driver,wait,amount,'short') #예약 취소 ~ 취소 완료
        except:
            if loop_count == 1:
                Module.Fail(title, num,'',driver)
                print("Fail 시점", datetime.now())
                break
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break


def test2():
    title = '[회원] 내륙 월렌트 1개월 결제 ~ 취소'
    num = 'TC'
    for loop_count in range(0, 2):
        try:
            Module.carmoreOpen(driver, wait)
            sleep(3)
            amount = Module_Script.L_Month_RentList(wait, driver, 1, who)
            Module.SimpleCardPay('m_dev', who, wait)
            # 결제완료
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제 완료"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카모아 국내 렌트카는 예약 즉시 확정됩니다!")]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"월 납부 금액")]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"대여/반납")]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
            sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="서비스 개선 설문조사"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="자차 대신에"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제출하기"]'))).click()
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]')))  # 렌트홈 진입 확인
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
            sleep(2)
            # 마이페이지
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마이페이지"]')))
            sleep(5)  # 예약 불러오는게 너무 느림
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약확정"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1개월")]'))).click()  # 예약카드 선택
            sleep(2)
            # 예약상세정보페이지
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 완료"]')))
            # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이메일로 예약 내역 받기"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="대여현황"]')))
            Module.while_loop( '//*[@text="결제 정보"]', driver, 'down_find', 1800)
            Module.while_loop( '//*[contains(@text,"결제성공")]', driver, 'down_find', 1800)
            Module.while_loop( '//*[contains(@text,"월 납부 금액(보험포함)")]', driver,  'down_find', 1800)
            Module.cancel_Process(wait, driver, wait, str(amount), 'month')  # 예약 취소 ~ 취소 완료
        except:
            if loop_count == 1:
                Module.Fail(title, num,'https://teamo2co.atlassian.net/browse/QA-1855',driver)
                print("Fail 시점", datetime.now())
                break
            else:
                print('첫 시도 Fail 사유')
                print("Fail 시점", datetime.now())
        else:
            Module.Pass(title, num,'')
            print("Pass 시점", datetime.now())
            break

def test3():
    title = '[회원] 일본 히카리 API 결제 ~ 취소'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        sleep(3)
        amount = Module_Script.L_Overseas_RentList(wait, driver, 'carmore', 'hikari_dev')
        Module.SimpleCardPay('o_dev', 'carmore', wait)
        # 결제완료
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 확인"]')))  # 국내는 '결제 완료', 해외는 '예약 확인'
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"바우처 받으실 이메일 :")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"잠깐! 호텔은 예약하셨나요?")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
        sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="서비스 개선 설문조사"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="여행"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제출하기"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]')))  # 렌트홈 진입 확인
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
        sleep(2)
        # 마이페이지
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마이페이지"]')))
        sleep(5)  # 예약 불러오는게 너무 느림
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"확정")])')))
        except:
            sleep(20) #접수상태라 시간 넉넉히 주고 수행
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"총 결제 금액")])[1]'))).click()

        # 예약상세정보페이지
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세"]')))
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"다운로드")]'))) #확정이 되어야 나오는 바우처 다운로드 받기 버튼 체크
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"접수")]')))  # 접수 케이스 일 경우
            driver.back()
            wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"총 결제 금액")])[1]'))).click()
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"다운로드")]')))
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[@text="결제 정보"]', driver, 'down_find', 1800)
        Module.down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        Module.while_loop('//*[contains(@text,"간편카드결제")]', driver, 'down_find', 1800)
        Module.while_loop('//*[contains(@text,"보험 및 플랜요금(")]', driver, 'down_find', 1800)
        Module.down_swipe(driver)
        Module.down_swipe(driver) #좀 밑에 있어서 넣어줌
        Module.while_loop('//*[contains(@text,"잠깐! 호텔은")]', driver, 'down_find', 1800)
        Module.cancel_Process(wait, driver, wait, amount, 'hikari')  # 예약 취소 ~ 취소 완료
        # ---------------------------테스트 완료 slack 발송
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())

def test4():
    title = '[회원] 호텔 결제 ~ 취소'
    num = 'TC'
    try:
        Module.carmoreOpen(driver, wait)
        sleep(3)
        amount = Module_Script.hotelMore(wait, driver, 'l_ht_dev','부산')
        Module.SimpleCardPay('h_dev', 'carmore', wait)
        # 결제완료
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제 완료"]')))  # 국내,호텔은 '결제 완료', 해외는 '예약 확인'
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"바우처 다운로드 받기")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"저렴하게 이동하세요")]'))) #렌트카 크로스셀 영역
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
        # 설문조사
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"설문")]')))
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="신혼여행"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="지인 추천"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="제출하기"]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
        sleep(2)
        # 마이페이지
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마이페이지"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="호텔"])[1]'))).click()
        sleep(5)  # 예약 불러오는게 너무 느림
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약확정"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"HT")]'))).click()
        sleep(2)
        # 예약상세정보페이지
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약자 정보"]')))
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[@text="결제 정보"]', driver, 'down_find', 1500)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"간편카드결제")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔 숙박 요금")]')))
        Module.while_loop('//*[contains(@text,"세금 및 수수료")]', driver,'down_find', 1500)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[contains(@text,"패밀리 라운지")]', driver,'down_find', 1800)
        Module.cancel_Process(wait, driver, wait, amount, 'hotel')  # 예약 취소 ~ 취소 완료
        #---------------------------테스트 완료 slack 발송
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())
    except:
        Module.Fail(title, num, '',driver)
        print("Fail 시점", datetime.now())


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
