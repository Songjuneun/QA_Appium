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
import os
import getpass
import Module
username = getpass.getuser()
now = datetime.now()
# ------------------------------------------------------------------------------------------------------------------- 공통 사용 스크렙트 모듈
def setup(wait,purchase):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="내일 다시 볼게요!"]'))).click()
    except:
        pass
    sleep(2)
    if purchase != 'tmap':
        # 로그인 되어 있는지 먼저 확인
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="My"]'))).click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약내역")]')))
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"로그인 하기")]'))).click()
            Module.login(wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외렌트")]')))


# ------------------------------------------------------------------------------------------------------------------- 제주 스크립트 모듈
def L_Jeju_RentList(wait,purchase,driver): #제주 차량리스트 확인용 스크립트 : 차량리스트 > 차량상세 > 결제 정보 > 카카오페이 연결 > 최근 본 상품
    setup(wait, purchase)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"단기렌트")]'))).click()  # 하단 단기렌트 탭하여 이동\
    sleep(2)
    Module.select_Region(wait, '제주', '제주국제공항')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]'))).click()
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"전체 보험")]'))) #차량리스트 진입 확인
    first_car = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[1]'))).get_attribute("text")
    one = first_car.replace('원 부터', '')  # 원 제거
    print('첫번째 차량 최저 가격 :', one)
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"' + one + '")])[2]'))).click()
    sleep(4)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="대여조건"]')))
        sleep(3)
        print("제주 depth2 진입")
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"포함가")])[1]'))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + one + '")]')))
    if purchase == 'yes':
        pass
    else:
        driver.back()
        driver.back()
        driver.back()#렌트카
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"종료")]')))
            driver.back()
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"렌트카")]'))).click()  # 렌트카 선택하니까 호텔이 눌림(?)
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"최근 검색")]')))
        Module.while_loop('//*[contains(@text,"최근 본 상품")]', driver, 'down_click', 1800)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + one + '")]'))).click()
        sleep(2)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + one + '")]')))
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"마감")]')))
    if purchase == 'tmap':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"바로 예약하기")]'))).click() #티맵 렌터카(슈퍼특가 없음)
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"렌트카")]'))).click() #카모아
    sleep(5)
    # 결제정보
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이름"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + one + '")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("팀오투테스트")
    amount = one

    return amount
#------------------------------------------------------------------------------------------------------------------- 내륙 스크립트 모듈
def L_City_RentList(wait,driver,who):
    #로그인 되어 있는지 먼저 확인
    setup(wait,who)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"29일")]'))).click()
    sleep(2)
    Module.select_Region(wait, '내륙', '인천')
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"24시간")]')))
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]'))).click()
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포함가")]')))
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"즉시할인")]'))) # % 있는거랑 같은 의미
        flag='a'
    except:
        flag='b'
    if flag == 'a':
        amount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"0원")])[4]'))).get_attribute("text")  # 차량 금액
        print(amount)
    else:
        amount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"0원")])[2]'))).get_attribute("text")  # 차량 금액
        print(amount)
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"포함가")])[1]'))).click()
    sleep(3)
    # 차량상세
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"자차")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포함가")]')))
    Module.down_swipe(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]'))).click()
    #취소수수료
    if Module.argv() != 'dev':
        #제외사유 : 개발서버 데이터가 실섭과 상이함
        Module.while_loop('//*[@text="취소규정"]', driver, 'down_click', 1800)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소규정 자세히 보기"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소 수수료"]')))
        Module.Cancel_table(wait, 'seoul')
        Module.down_swipe(driver)
        sleep(3)
        #제외사유 : 개발서버 테스트 시 시간이 너무 오래 걸림
        Module.while_loop('//*[contains(@text,"staticMap")]', driver, 'down_click', 1500)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="지점 지도 보기"]'))) #선택 못할 경우가 발생함
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="길찾기"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="주소복사"]')))
        driver.back()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"렌트카")]'))).click()
    # 결제정보
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이름"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("팀오투테스트")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
    if Module.argv() == 'dev':
        Module.Insert_info(wait, driver)

    return amount
#-------------------------------------------------------------------------------------------------------------------해외렌트 스크립트 모듈
def L_Overseas_RentList(wait,driver,who,type):
    # type : direct = 괌 / 해외 직판, hikari = 후쿠오카 / 히카리 api, sicily = 로마 테르미니역 / 시실리 api, api = LAX / 버젯 or 클룩 api / cash = LAX / 클룩 api 현장결제 / 개발서버 결제 = hikari_dev
    # purhcase : tmap = 티맵 렌터카
    setup(wait,who)
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]'))).click()
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외렌트")]'))).click()
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"곳으로")]')))
    if type == 'direct':
        Module.select_Region(wait, '미국', 'LAX')
    elif type == 'hikari' or type == 'hikari_dev':
        Module.select_Region(wait, '일본', '후쿠오카 공항')
    elif type == 'api' or type == 'cash':
        Module.select_Region(wait, '이탈리아', '로마')
    elif type == 'sicily':
        Module.select_Region(wait, '이탈리아', '로마')
    elif type == 'cash':
        Module.select_Region(wait, '미국', 'LAX')
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"24시간")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]'))).click()
    # 차량리스트_필터 적용
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.o_rolling + '"]')))
    sleep(10) #api 호출 기다리기
    if type == 'cash':
        sleep(5) #더 기다리기
    select = '' #히카리와 유럽카 구분 시 사용
    if type != 'api':
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"필터")]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"결제조건")]')))
        Module.down_swipe(driver)
        if type == 'direct':
            Module.while_loop('//android.widget.CheckBox[contains(@text,"자차플러스+")]', driver, 'down_click', 1800)
        elif type == 'hikari':
            if Module.argv() != 'dev':
                Module.while_loop('//android.widget.CheckBox[contains(@text,"니코니코")]', driver, 'down_click', 2000) #도요타 잘 안 보임
                select = '토요타'
            else:
                wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.CheckBox[contains(@text,"Europcar")]'))).click()
                select = '유럽카'
        elif type == 'cash':
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.TextView[@text="현장결제"]'))).click()
        elif type == 'sicily':
            Module.while_loop('//android.widget.CheckBox[contains(@text,"Sicily by Car")]', driver, 'down_click', 2000)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="적용"]'))).click()
    sleep(3)
    #차량리스트
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포함가")]')))
    if type == 'direct':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"자차플러스")]')))
    num = 2
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"즉시할인")]')))
        num = num+1
    except:
        pass
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"%")]')))
        num = num+1
    except:
        pass
    amount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"0원")])['+str(num)+']'))).get_attribute("text")
    print('차량 금액 :',amount)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"포함가")]'))).click()
    sleep(3)
    # 차량상세
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포함가")]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
    # 차량상세 _ 추가옵션션
    Module.addOn('차량상세', wait, driver, type, select)
    Module.down_swipe(driver) #카텔 배너 생기면서 스와이프 필요해짐
    if type != 'hikari_dev':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]'))).click()
        # 차량상세_취소규정
        Module.while_loop('//*[@text="취소규정"]', driver, 'down_click', 1800)
        if type == 'direct':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소규정 자세히 보기"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소 수수료"]')))
            Module.Cancel_table(wait, 'guam')
        elif type == 'hikari':
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"무료")]')))
        # 차량상세_업체정보_지도
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[contains(@resource-id,"sci_map_branch_oversea")]', driver, 'down_find', 1800)
        location = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@resource-id,"sci_map_branch_oversea")]'))).location
        sleep(2)
        print(location)
        TouchAction(driver).tap(x=location['x'] + 100, y=location['y'] + 100).perform()  # Galaxy S10 5G 단말 맞춤 시작하기 버튼 좌표 직접 클릭
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="지점 지도 보기"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="길찾기"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="주소복사"]')))
        driver.back()
    # 차량상세_결제 CTA 버튼
    if who == 'tmap' or type =='cash':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"예약하기")]'))).click()  # 티맵 렌터카(호텔 없음), 현장결제(패키지 불가)
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"렌트카")]'))).click()  # 카모아
    # 결제정보
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="신분증(여권)과 동일한 이름을 입력해 주세요."]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("TEST")
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[2]'))).send_keys("Automation")
    Module.down_swipe(driver)
    if type == 'direct':
        Module.while_loop('//android.widget.Image[@text="handle"]', driver, 'down_find', 1800)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="USD 500"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"11,990")]')))
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"23,990")]'))) # 괌 reach rentcal USD 2,500 설정함
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[@text="(필수) 렌터카 직원을 만나는 장소를 선택해주세요."]', driver, 'down_click', 1800)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"사무실")]'))).click()
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"주소")]'))).click()
        Module.while_loop('//*[@text="(필수) 차량 반납 방법을 선택해주세요."]', driver, 'down_click', 1800)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"사무실")]'))).click()
        except:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"주소")]'))).click()
    elif type == 'cash':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"0원")]')))  # 결제 진행 팝업 온라인 결제 0원 노출
    else:
        Module.addOn('결제정보', wait, driver, type, select) #히카리, 유럽카, 시실리에서만 추가 옵션 검증하도록 되어있는 모듈
    if type == 'hikari':
        Module.while_loop('//*[@text="인원수 선택"]', driver, 'down_click', 1800)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="2"]'))).click()
        sleep(2)
    return amount

#-------------------------------------------------------------------------------------------------------------------월렌트 스크립트 모듈

def L_Month_RentList(wait,driver,date,who):
    setup(wait,who)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"홈")]'))).click()
    sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"월렌트")]'))).click()  # 차량 리스트에서 클릭할 때
    sleep(5)
    Module.select_Region(wait, '내륙', '인천')
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"1개월")]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"실시간 최저가 차량 검색")]'))).click()
    sleep(4)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.m_rolling + '"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Image)[5]')))  # 첫번째 차량 이미지 노출 확인
    lowamount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[1]'))).get_attribute("text")  # 개월 수 중 최소 대여 금액
    checkamount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[2]'))).get_attribute("text")  # 개월 수 중 최소 대여 금액
    lowamount = int(re.sub(r"[^0-9]", "", lowamount))
    checkamount = int(re.sub(r"[^0-9]", "", checkamount))
    # print("최소 금액=", lowamount)
    # print("비교 금액=", checkamount)
    if (lowamount < checkamount):
        gap = checkamount - lowamount
        gap = str(format(gap, ','))
        print('매달 ' + gap + '원 절약!')
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text ="매달 ' + gap + '원 절약!"]')))
        except:
            print("절약 금액 틀림!")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text ="강제 Fail 발생 스크립트"]')))
    else:
        print("절약 금액 없음!")
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[3]')))
    # depth2 로 갈 경우
    if date == 1:
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"1개월")])[2]'))).click()
    else:
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"3개월")])[1]'))).click()
    sleep(3)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH,'(//android.widget.Image)[4]')))  # 차량 이미지 확인wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="첫 구매 1만원 할인쿠폰 적용중"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="3개월"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.m_rolling + '"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"포함가")])[1]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="필독사항"]')))
    except:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="필독사항"]')))
    # 차량 상세
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Image)[3]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="차량 이미지는 이해를 돕기 위한 예시로, 배차 차량과 다를 수 있습니다."]')))
    Module.down_swipe(driver)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="필독사항"]'))).click()
    Module.while_loop('//*[@text="취소규정"]', driver, 'down_click', 1800)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소규정 자세히 보기"]'))).click()
    # 취소 수수료 표 텍스트 확인 하기------------------------------------------------------------------시작
    Module.Cancel_table(wait, 'month')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약하기")]'))).click()
    sleep(5)
    # 결제정보
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("팀오투테스트")
    amount = lowamount
    return amount

#-------------------------------------------------------------------------------------------------------------------호텔모아 스크립트 모듈

def hotelMore(wait,driver,type,region):
    #who : 티맵에 호텔이 없어서 필요없음
    #type : nl_ht_catel_pk (비 회원 호텔 단독 카텔 쿠폰에서 패키지로) , l_ht_dev (개발서버 회원 호텔), l_pK (회원 패키지) , l_rent_catel_pk (회원 차량상세 슈퍼특가 버튼 패키지로)
    if type != 'nl_ht_catel_pk' and type != 'l_rent_catel_pk':
        setup(wait,'no')
    else:
        if type == 'l_rent_catel_pk':
            pass
            # 차량 상세 단계에서 진행
        else:
            # 로그아웃 확인
            Module.logout(driver, wait)
    if type != 'l_rent_catel_pk': #차량상세를 통해 진입 시 호텔 검색 조건 입력 과정을 생략한다.
        #호텔 검색 조건 입력 과정
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"호텔")])[2]'))).click()  # 네비게이션 호텔 버튼
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="호텔모아"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"렌트카 10% 할인쿠폰 지급")]')))
        #호텔 지역 선택 : 인기 지역 부산으로 설정
        #버튼 index 0: 국내 호텔, 1: 해외 호텔, 2: 지역 버튼  (수정 시점 : 1.0.14 : 국내 호텔, 해외 호텔 나뉨)
        if region == '부산':
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@index=0]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@index=2]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 검색"]')))
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"location-pin")])[3]'))).click()
            sleep(2)
        else:
            # 후쿠오카 일 때
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@index=1]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@index=2]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 검색"]')))
            Module.down_swipe(driver)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 본 상품"]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image[@text="location-pin"])[12]'))).click()
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image[@text="location-pin"])[17]'))).click()
            sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"'+region+'")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"성인2")]')))
        #호텔 날짜 선택 : 설정되어 있을 경우가 안되어 있을 경우보다 많아 순서 조정
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"1박")]'))) #기본 날짜 설정으로 바뀜 : 1.0.14
        # 패키지 변환 절차
        if type == 'nl_ht_catel_pk' or type == 'l_ht_dev' :
            #패키지로 되어 있다면, 호텔로 변환 : 호텔 테스트용
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 숙소 검색"]'))).click()
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 렌트카+숙소 검색"]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"함께 예약")]'))).click()
                sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 숙소 검색"]'))).click()
        else:
            #호텔로 되어 있다면, 패키지로 변환 : 패키지 테스트용
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 렌트카+숙소 검색"]'))).click()
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 숙소 검색"]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"함께 예약")]'))).click()
                sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="실시간 최저가 렌트카+숙소 검색"]'))).click()
        if type != 'nl_ht_catel_pk':
            #카텔 쿠폰 팝업 조건을 만족할 경우
            try:
                sleep(5)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"기본순")]')))
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"쿠폰이 지급")]')))
                if type == 'l_ht_dev':
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"호텔만 구매")]'))).click()
                else:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="확인"]'))).click()
                sleep(5)
    # 리스트
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"필터")]')))
    # 리스트 노출 확인하기
    amount = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"총 ")]'))).get_attribute("text")
    amount = amount[-12:]  # 100만원 단위까지만 정제
    print('정제안한 amount', amount)
    amount = int(re.sub(r"[^0-9]", "", amount))  # 공백 없애기 작업 해주고
    amount = str(format(amount, ','))  # 다시 콤마 붙여주기
    print(amount)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + amount + '")]'))).click()
    if type == 'nl_ht_catel_pk':
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="쿠폰 없이 비회원으로 예약할래요"]'))).click()
        except:
            pass
    sleep(3)
    # 호텔 상세
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="상세정보"]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="view-all-thumbnails"]')))  # 모두보기 버튼
    hotel_name = wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView)[7]'))).get_attribute("text")  # 호텔 이름 추출(호텔 리스트에서 추출 불가 : 패밀리 특가 호텔이 1번째 일 경우 호텔 이름과 가격이 다른 현상 발생)
    print('호텔 이름:', hotel_name)
    if type == 'nl_ht_catel_pk':
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="카텔특가"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="쿠폰받기 쿠폰받기"]'))).click()
        sleep(2)
        Module.login(wait)
        sleep(2)
        # 호텔 상세 _ 카텔 쿠폰 발급 완료 모달 확인
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="쿠폰이 지급되었어요!"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="호텔+렌트카 함께 구매하러가기"]'))).click()
            sleep(2)
            # 패키지 호텔 상세로 이동함
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="예약중"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="발급완료 쿠폰받기"]')))
        except:
            # 이미 발급 받아져 있는 상태
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"이미 쿠폰을 보유")]')))
    else:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="객실목록"]')))
        Module.down_swipe(driver)
        Module.while_loop('//*[contains(@text,"' + amount + '")]', driver, 'down_find', 1800)
        Module.while_loop('//*[contains(@text,"객실 선택")]', driver, 'down_click', 1800)
        # 객실 상세
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="객실정보"]')))
        Module.while_loop('//*[contains(@text,"' + amount + '")]', driver, 'down_find', 1800)
        Module.down_swipe(driver)
        Module.while_loop('//*[contains(@text,"취소규정")]', driver, 'down_find', 1800)
        # 객실 상세 - 취소규정
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="날짜 및 시간 기준 : Asia/Seoul"]')))
        Module.down_swipe(driver)
        Module.while_loop('//*[@text="취소문의는 카모아 고객센터(1544-5344)로 문의 바랍니다."]', driver, 'down_find', 1800)
        Module.down_swipe(driver)
        Module.down_swipe(driver)
        Module.while_loop('//*[contains(@text,"요금 상세 정보")]', driver, 'down_find', 1800)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"호텔 숙박 요금")]')))
        if type != 'l_ht_dev':
            if region == '부산' or region =='제주':
                Module.while_loop('//*[contains(@text,"보험 요금(")]', driver, 'down_find', 1800) #국내
            else:
                Module.while_loop('//*[contains(@text,"보험 및 플랜 요금(")]', driver, 'down_find', 1800) #해외
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"세금 및 수수료")]')))
        Module.while_loop('//*[contains(@text,"총 결제금액")]', driver, 'down_find', 1800)
        if type != 'l_ht_dev':
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"호텔+렌트카")]'))) #cta 문구
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"바로 예약하기")]'))).click()  # 호텔 : 결제 정보로 이동, 패키지 : 예약 정보 확인으로 이동
        if type != 'l_ht_dev':
            # 예약정보 확인으로 이동 시
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="객실정보"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="렌트카 정보"]')))
            if type != 'l_rent_catel_pk':
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="카모아 추천차량!"]')))
            # 4월 1일 -> 결제 버튼 클릭하는거 만들기
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="호텔 정보를 확인했어요 다음"]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="렌트카 정보를 확인했어요 다음"]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"호텔+렌트카")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"바로 예약하기")]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"선택하신 호텔 및 렌트카가 맞나요?")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="확인"]'))).click()
        sleep(5)
        # 결제 정보
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="결제정보"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="성인 2명"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + hotel_name + '")]')))
        if type != 'l_ht_dev':
            if region == '부산' or region == '제주':
                Module.Hotel_Insert_info('korea', wait, driver, 'package')
            else:
                Module.Hotel_Insert_info('overseas', wait, driver, 'package')
        else:
            Module.Hotel_Insert_info('h_dev', wait, driver, 'solo')
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
    return amount
