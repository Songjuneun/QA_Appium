from appium import webdriver
from time import *
import datetime
from datetime import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Open iOS simulator 11.2 and install TestApp
import os
import Module
import getpass
username = getpass.getuser()
now = datetime.now()
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))
wait = WebDriverWait(driver,Module.wait_sec())

def test1():
    global flag
    title = '[비 회원] 제주 단기렌트 야간인수 반납불가 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"단기렌트")]'))).click()
        sleep(3)
        Module.select_Region(wait,'제주','제주국제공항')
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"24시간")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Button)[5]'))).click() #날짜 및 시간 버튼 클릭
        sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"날짜 및 시간 선택")]')))
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@text="10:00"])[3]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="10:00"]')))
        Module.while_loop('//*[@text="22:30"]', driver, 'down_click', 2300)
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"반납불가")]')))
        # 날짜 및 시간 선택 모달 닫기
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="close-modal"]'))).click()
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test2():
    title = '[비 회원] 월렌트 1개월 차량 리스트, 차량 상세 (취소 규정 확인), 결제 정보'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]')))
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"월렌트")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.m_rolling + '"]')))
        lowamount = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"원 부터")])[1]'))).get_attribute("text")
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[contains(@text,"' + lowamount + '")])[2]'))).click()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"포함가")]'))).click() #보험 이름 미 노출 정상 상태
        except:
            pass
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰 없이 비회원으로 예약할래요"]'))).click()
        except:
            pass
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"대여규정")]')))
        Module.while_loop('//*[@text="취소규정"]', driver,'down_click',1800)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소규정 자세히 보기"]'))).click()
        # 취소 수수료 표 텍스트 확인 하기------------------------------------------------------------------시작
        Module.Cancel_table(wait, 'month')
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"바로 예약")]'))).click()
        # 결제정보
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="운전자 정보"]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test3():  # 없음
    title = '[비 회원] 렌트카 해외렌트 페이지 & 괌 인기차량 조회 후 최근 검색 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외렌트")]'))).click()
        sleep(4)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="만 30 ~ 65세"]')))
        Module.down_swipe(driver)
        sleep(2)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"본 상품")]')))
            Module.down_swipe(driver)
        except:
            pass
        Module.while_loop('//*[@text="괌"]', driver, 'down_click', 1500)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"괌")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"사이판")]')))
        bestCar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"쾌속")]')))
        carname = str(bestCar.get_attribute("text"))[0:4]
        print(carname)
        sleep(3)
        bestCar.click()
        sleep(3)
        # 차량리스트 확인
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"' + carname + '")])[1]')))  # 필터에 노출 되는지
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="' + Module.o_rolling + '"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"픽업/드롭")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"첫 구매 할인")]')))
            # 제주 필터링 차량리스트 확인
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"' + carname + '")])[2]')))  # 차량 카드에도 노출되는지
        except:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"해당 필터 조건에 맞는 차량이 없습니다.")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"필터 초기화")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click()  # 뒤로가기 버튼 클릭
        # 렌트카 최근 검색 부산/동구 저장 확인
        Module.up_swipe(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 검색"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"픽업/드롭")]'))) #괌 검색 내역
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"삭제 버튼")]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test4():
    title = '[비 회원] 해외API 1일 차량 리스트, 차량 상세 (취소 규정 확인), 결제 정보 '
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외렌트")]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실시간 최저가 차량 검색"]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="' + Module.o_rolling + '"]')))
        sleep(3)
        Module.while_loop('(//*[contains(@text,"포함가")])[1]', driver, 'down_click', 1800)
        sleep(3)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰 없이 비회원으로 예약할래요"]'))).click()
        except:
            pass
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="필독사항"]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test5():
    title = '[비 회원] 렌트카 단기렌트 페이지 & 부산 인기차량 확인'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"단기렌트")]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"24시간")]')))
        Module.while_loop( '//*[@text="경북"]', driver,'down_click', 1500) #개발, 실섭, STG 다 있는 지역
        if Module.argv() == ('live' or 'stage'):
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"제주")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"전남")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"경북")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"서울")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"강릉")]')))
        else:
            print("개발서버니까 미 노출")
        sleep(2)
        bestCar = wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"년식")])[1]'))) #년식 ~ 노출되는 첫번째 차량 카드
        carname = str(bestCar.get_attribute("text"))[0:4]
        print(carname)
        bestCar.click()  # Default = 제주 인기차량 첫번째 차량 카드 클릭
        sleep(3)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"경주")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"' + carname + '")])[1]')))  # 필터에 노출 되는지
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="' + Module.k_rolling + '"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"경주")]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"첫 구매 할인")]')))
            #제주 필터링 차량리스트 확인
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"' + carname + '")])[2]'))) #차량 카드에도 노출되는지
        except:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"해당 필터 조건에 맞는 차량이 없습니다.")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"필터 초기화")]')))
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"마감되었습니다.")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.Image)[1]'))).click() #뒤로가기 버튼 클릭
        Module.up_swipe(driver)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 검색"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"삭제 버튼")]')))  # 텍스트 워딩 변경됨 11/17
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"경북 / 경주")]'))).click()
        sleep(3)
        #최근 검색으로 차량리스트 진입하기
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"경주")]')))
        checkdate, checkdate2 = Module.check_Date(now,1)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"'+checkdate2+'")]'))) #다음날짜로 검색하는게 default 값이라 고정
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"10:00")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"' + carname + '")])[1]')))
        driver.back()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()

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
    test4()
    test5()
