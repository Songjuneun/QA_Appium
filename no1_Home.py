from appium import webdriver
from time import *
import datetime
from datetime import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import Module
now = datetime.now()
# Connect to Appium server on local host
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('yes'))
wait = WebDriverWait(driver,Module.wait_sec())
# Test cases
def test1():
    title='앱 최초 실행 권한 허용 ~ 홈 화면 진입'
    num = 'TC'
    try:
        Module.carmoreOpen(driver,wait)
        wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="모든 권한 허용하기"]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="앱 사용 중에만 허용"]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="허용"]'))).click()  # 4.1.28 부터 생김
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="허용"]'))).click()  # 알림 허용
        except:
            pass
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="모두 허용"]'))).click() #4.1.46 부터 생김
        sleep(2)
        TouchAction(driver).tap(x=540, y=1971).perform()  # Galaxy S10 5G 단말 맞춤 시작하기 버튼 좌표 직접 클릭
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
        # 뜨면 닫고
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="닫기"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="내일 다시 볼게요!"]'))).click()
        except:
            print("메인 팝업이 없습니다. - 진짜 없는건지 확인 필요 ")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"모두보기")]')))
        #최저가보장 뱃지 확인
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="최저가보장"])[1]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="최저가보장"])[2]')))
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test2():
    title='홈 > 메인 이벤트 배너 > 모두보기 클릭 > 이벤트 페이지 이동 확인'
    num = 'TC'
    try:
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"홈")]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"모두보기")]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이벤트"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Button)[1]'))) #이벤트 리스트 첫번째
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Button)[2]'))) #이벤트 리스트 두번째
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        sleep(2)
        #앱 꺼지는 현상 발생 : 1120
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="호텔모아"]')))
        # 9월 -------
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="KTO_STAR_이미지"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"숙박페스타")]')))
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카모아_신규_서비스_항목")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"렌트카와 결합할인")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"여행자 보험 국내 해외 모두 여행자 보험")]')))
        price_gurantee=['렌트카 최저가를 보장합니다!','300%를 보상 해드립니다']
        for i in range (len(price_gurantee)):
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"'+price_gurantee[i]+'")]'))) # 최저가 보장 띠 배너 -모바일만 노출
                break
            except:
                pass
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test3():
    title = '홈 > 패밀리 혜택 라운지 버튼 > 비 회원 전용 패밀리 라운지 페이지로 이동 확인'
    num = 'TC'
    try:
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        Module.down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="패밀리 혜택 바로가기 패밀리 혜택"]'))).click()
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="카모아 패밀리 라운지"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="3초 회원가입하고 패밀리 혜택받자!"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="공항 라운지"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Image)[1]'))).click() #뒤로가기 버튼 클릭
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"친구초대")]')))  # 홈 이동 확인
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test4():
    title = '홈 > 쿠폰함 버튼 > 비 회원 전용 로그인 모달 노출'
    num = 'TC'
    try:
        sleep(3)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰함 바로가기 쿠폰함"]'))).click()
        except:
            Module.down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="쿠폰함 바로가기 쿠폰함"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"3초 가입/로그인 시 추가 할인")]')))  # 홈 이동 확인
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"네이버로 로그인")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카카오톡으로 로그인")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"Apple로 로그인")]')))
        driver.back()
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test5():
    title = '홈 > 친구초대 버튼 > 친구초대 전용 페이지로 이동 확인'
    num = 'TC'

    try:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="친구초대 바로가기 친구초대"]'))).click()
        except:
            Module.down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="친구초대 바로가기 친구초대"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"로그인이 필요한 서비스입니다.")]')))  # 이벤트 리스트 첫번째
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="로그인"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"네이버로 로그인")]')))
        driver.back() #로그인 모달 닫기
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"쿠폰함")]')))  # 홈 이동 확인 #FE-2568에서 작업됨
        driver.back()  # 로그인 모달 닫기
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())

def test6():
    title = '홈 > Foreigner 버튼 > Foreigner 이벤트 상세 페이지로 이동 확인'
    num = 'TC'

    try:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="Foreigner 바로가기 Foreigner"]'))).click()
        except:
            Module.down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="Foreigner 바로가기 Foreigner"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이벤트 상세"]')))  # 이벤트 리스트 첫번째
        driver.back()
        sleep(2)
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test7():
    title = '[비 회원] 여행자 보험 배너 클릭 시 보험 페이지로 이동하는지 확인하기 '
    num = 'TC'
    try:
        sleep(4)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="렌트카"]')))
        Module.down_swipe(driver)
        Module.while_loop( '//android.widget.Image[@text="보험서비스"]', driver, 'down_click', 1500)
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"여행자 보험")]'))).click()
        sleep(3)
        # 보험 페이지
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"국내 이동에 추천")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"해외 여행에 추천")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Image[@text="go back"]'))).click()
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        driver.back()
    except:
        Module.Fail(title, num, '', driver)
        print("Fail 시점", datetime.now())
    else:
        Module.Pass(title, num, '')
        print("Pass 시점", datetime.now())


def test8():
    title = '홈 > 채널톡 확인'
    num = 'TC'
    try:
        sleep(4)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        sleep(4)
        wait.until(EC.element_to_be_clickable((By.ID, 'com.gogocarhome.gogocar:id/ch_imageChannelButtonFace'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"안녕하세요.")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@resource-id="com.gogocarhome.gogocar:id/ch_imageLeftBezierButton"]'))).click()
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
    test6()
    test7()
    test8()



