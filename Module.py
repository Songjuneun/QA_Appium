
from time import *
import getpass
import traceback
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pyautogui
from slacker import Slacker
from datetime import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import sys
from datetime import *

username = getpass.getuser()
carmore_store = '/Users/' + username + '/Downloads/렌트카 카모아 - 국내 해외 렌터카 1등_4.1.29_Apkpure.apk'
carmore_test = '/Users/' + username + '/Downloads/dev_carmore_4.1.36.apk'
tmap ='/Users/' + username + '/Downloads/TMAP  10.0.0.291979.apk'
now = datetime.now()
if username == 'joy':
    # Galaxy S23+
    deviceID = '192.168.0.255:5555'
    deviceName = 'S23+'
    platformVersion = '14'
    # Galaxy S10
    # deviceID = '192.168.0.127:5555'
    # platformVersion = '12'
    # deviceName = 'S10'
def wait_sec():
    server = argv()
    if server == 'dev':
        wait_sec = 20
    else:
        wait_sec = 15
    return int(wait_sec)
# elif username == 'levi': #elif를 통해 levi 추가(levi)
#      deviceID = '192.168.1.4:5555'
#      platformVersion = '13'
#      deviceName = 'S23'
# else:
#     deviceID = '192.168.0.228:5555'
def argv():
    return f"{sys.argv[1]}"
#------------------------------------------- slack post message_start ----------------------------------------------------------------------------------
slack_token = '{slack api token}'
client = WebClient(token=slack_token)
channel_id = "#qa_android_자동화테스트_결과"
slack = Slacker(slack_token)
if argv() == 'live' or argv() == 'tmap':
    title = '[Live][상시] 리그레션 자동화 테스트'
elif argv() == 'stage':
    title = '[STAGE][] 리그레션 자동화 테스트'
else:
    title = '[DEV][결제정보_리팩토링] 리그레션 자동화 테스트'

def slack_post(result): #pass용
    slack.chat.post_message('#qa_android_자동화테스트_결과', str(result), title , None, None, None, None, None,None, None, ':arong:')
    # pass

def slack_post_img(file_path,result): #fail용
    # print('이미지 주석 처리 중')
    response = client.files_upload(
        channels=channel_id,
        file=file_path,
        title=str(now),
        initial_comment =str(result)
    )
    # 전송 후 응답 출력
    print(f"File uploaded: {response['file']['id']}")

#------------------------------------------- slack post message_end ----------------------------------------------------------------------------------

def carmoreOpen(driver,wait):
    server = argv()
    driver.terminate_app('com.gogocarhome.gogocar')
    driver.activate_app('com.gogocarhome.gogocar')
    sleep(3)
    if server == 'live':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실서버"]'))).click()
    elif server == 'stage':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="스테이징서버"]'))).click()
    elif server == 'dev':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="개발 1서버"]'))).click()
    sleep(2)
    wait.until(EC.presence_of_element_located((By.ID, 'android:id/button1'))).click()
    # if server == 'live':
    #     sleep(4)
    #     try:
    #         wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
    #         wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"-")]')))  # 개발서버로 드러와짐
    #     except:
    #         driver.terminate_app('com.gogocarhome.gogocar')
    #         driver.activate_app('com.gogocarhome.gogocar')
    #         sleep(3)
    #         if server == 'live':
    #             wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실서버"]'))).click()
    #         elif server == 'stage':
    #             wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="스테이징서버"]'))).click()
    #         elif server == 'dev':
    #             wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="개발 1서버"]'))).click()
    #         sleep(1)
    #         wait.until(EC.presence_of_element_located((By.ID, 'android:id/button1'))).click()

    #서버 첫 시작 케이스 때문에 홈 검증 없애야함.

def tmapOpen(driver,wait):
    driver.terminate_app('com.skt.tmap.ku')
    driver.activate_app('com.skt.tmap.ku')
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"오늘은 그만보기")]'))).click()# 두번 노출될 가능성 있음.
    except:
        pass
    # 렌터카 클릭하기
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="렌터카"]'))).click()
    sleep(2)
    # 카모아 진입 확인
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"단기렌트")]')))
    print("Module-T-exception 완료")

def login(wait):
    sleep(3)#너무 빨리 눌리면 안됨
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카카오톡으로 로그인")]'))).click()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"즐거운 여정 시작하기")]'))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="닫기"]'))).click()
    # sleep(3)  # 너무 빨리 눌리면 안됨
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"네이버로 로그인")]'))).click()
    # sleep(3)
    # try:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="joyto2"]'))).click()
    # except:
    #     pass
    # try:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="닫기"]'))).click()
    # except:
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"즐거운 여정 시작하기")]'))).click()

def logout(driver,wait):
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"홈")]'))).click()
    sleep(3)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[contains(@text,"My")]'))).click()
    try:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@text="가입 / 로그인 하기"]')))
        print("이미 로그아웃 되어 있음")
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="마이페이지"]')))
        down_swipe(driver)
        down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="내 정보 관리"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="로그아웃"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click() #로그아웃 최종 확인 모달임. 
        if argv() == 'live':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실서버"]'))).click()
        elif argv() == 'stage':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="스테이징서버"]'))).click()
        elif argv() == 'dev':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="개발 1서버"]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.ID, 'android:id/button1'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="홈"]')))
    print("Module-logout 완료")

# 세션 유지 후 앱 실행
def Setting_Reset(reset):
    if reset == 'yes':
        #카모아 리셋 버전
        desired_caps = {
            'app': carmore_test,
            'platformName': 'Android',
            'platformVersion': platformVersion,
            'deviceName': deviceName,
            'automationName': 'Uiautomator2',
            'appPackage': 'com.gogocarhome.gogocar',
            'deviceID': deviceID,
            "noReset": "false"
        }
    elif reset == 'no':
        #카모아 노리셋 버전
        desired_caps = {
            'app': carmore_test,
            'platformName': 'Android',
            'platformVersion': platformVersion,
            'deviceName': deviceName,
            'automationName': 'Uiautomator2',
            'appPackage': 'com.gogocarhome.gogocar',
            'deviceID': deviceID,
            "noReset": "true"
        }
    elif reset == 'iOS':
        #카모아 노리셋 버전
        desired_caps = {
            'platformName': 'iOS',
        'platformVersion': platformVersion,
        'deviceName': 'iPhone 14',
        'bundleId' : 'com.gogocarhome.gogocar',
        'automationName': 'XCUITest',
        'derivedDataPath': '/Users/joy/Library/Developer/Xcode/DerivedData/WebDriverAgent-abcjmkukewwerubwcraubcqwzqke',
        'udid': '00008110-00080D261A06201E',
        "noReset": False
        }
    else:
        #티맵 렌터카
        desired_caps = {
            'app': tmap,
            'platformName': 'Android',
            'platformVersion': platformVersion,
            'deviceName': deviceName,
            'automationName': 'Uiautomator2',
            'appPackage': 'com.skt.tmap.ku',
            # 'udid': 'R3CM606KAJL',
            'deviceID': deviceID,
            "noReset": "true"
        }

    return desired_caps

def select_Region(wait,step1,step2):
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.Button)[4]'))).click()
    if step1 == '미국' or step1 == '일본' or step1 == '이탈리아':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="해외 지역 선택"]')))
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="국내 지역 선택"]')))
    if step1 == '제주':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="' + step1 + ' ' + step1 + '"]'))).click()
    sleep(2)
    if step2 == 'LAX':
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외 지역명, 역")]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("LAX")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"Los Angeles")])[1]'))).click()
    if step2 == '괌':
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외 지역명, 역")]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("괌")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"Guam")])[1]'))).click()
    elif step2 == '제주국제공항':
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"제주도 전체")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="제주국제공항"]')))
    elif step2 == '인천':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="인천"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="서구"]'))).click()
    elif step2 == '후쿠오카 공항':
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외 지역명, 역")]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("후쿠오카")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[contains(@text,"Airport")])[1]'))).click()

    elif step2 == '로마':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"해외 지역명, 역")]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("로마")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"로마 테르미니역")]'))).click()

def Payment(what,wait,who,pay):
    #what = 'ktx','jeju','k_short', 'month', 'overseas'
    if what == 'jeju' or what == 'k_short' or what == 'month' or what == 'solo' or what == 'package' or what == 'k_dev' or what == 'm_dev' or what =='h_dev':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"결제하기")]'))).click() #단기렌트, 월렌트
    elif what == 'o_short_direct' or what == 'o_short_api'or what == 'o_dev' :
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[contains(@text,"예약하기")]'))).click() #해외렌트
    elif what == 'insurance':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]'))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예매하기")]'))).click() #ktx
    sleep(3)
    ansim ='no check'
    ansim_amount = '0'
    if what == 'jeju' or what == 'k_short' or what == 'k_dev' or what == 'o_short_direct':
        # 안심플러스 팝업 확인하기
        if (what == 'jeju' or what == 'k_short' or what == 'k_dev') and who =='carmore':
            sleep(2)
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="안심플러스⁺로 안전한 휴가 보내세요!"]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="1인"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="1,900원"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="[필수] 가입 안내 및 개인정보 처리 동의"]'))).click()
                sleep(2)
                if what == 'k_dev':
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="안심플러스⁺ 하고 혜택받기"]'))).click()
                    ansim = 'check'
                    ansim_amount = '1900'
                else:
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="혜택 받지 않기"]'))).click()
            except:
                print("안심플러스 미 판매 조건인지 확인 필요")
        else:
            print('티매 렌터카 안심플러스 미 판매')
        # 자차플러스 팝업 확인하기
        if ansim == 'check':
            print("안심플러스 체크해서 자차플러스 팝업 미 확인")
        else:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="자차플러스하고 혜택 받기"]')))
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="혜택 받지 않기"]'))).click() #정형화되었을 때 뜨는 팝업 (제주 리본/파트너스 , 내륙 아직 미적용)
            except:
                print("자차플러스 미 판매 업체")
    else:
        print('안심플러스 자차플러스 미 판매 렌트타입')
    # 최종 결제 확인 모달 결제하기 클릭 (보험, 호텔은 없음)
    if what == 'insurance' or what == 'package' or what == 'solo' or what == 'h_dev':
        pass
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="차량정보"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제하기"]'))).click()
    sleep(3)
    #토스 위젯 진입
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제 방법"]')))
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="'+pay+'"]'))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"더보기")]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="'+pay+'"]'))).click()
    if pay == '신용·체크카드':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="카카오뱅크"]')))
        if what != 'k_dev' and what != 'o_dev' and what != 'm_dev' and what != 'h_dev':
            print('결제하기 테스트를 하면 안되는 애들')
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="농협"]'))).click()
        else:
            print('개발서버다 결제하기 테스트 고고')
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="국민"]'))).click()
            if who == 'carmore':
                wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="결제하기"]'))).click()  # 카모아
                print('카모아 전용 결제하기 누름')
            else:
                wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="결제하기"])[2]'))).click()  # 티맵
                print('티맵 전용 결제하기 누름')
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="앱 없이 결제"]'))).click()
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="간편 로그인"]')))
            wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("01074714756") #휴대폰번호
            wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).send_keys("9710212") #주민등록번호 앞 7자리
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="개인정보 수집이용 동의"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="로그인"]'))).click()
            sleep(2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="포인트리"]')))
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제하기"]'))).click()
            key = [7,8,5,8,4,8]
            for i in range (0,7):
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text='+str(key[i])+']'))).click()
    if pay == '간편카드결제':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="일시불"]')))
        if what != 'k_dev' and what != 'o_dev' and what != 'm_dev' and what != 'h_dev':
            print('결제하기 테스트를 하면 안되는 애들')
        else:
            sleep(5)
            print('개발서버만 들어올 수 있는 결제 버튼')
            if who == 'carmore':
                wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="결제하기"]'))).click()  # 카모아
                print('카모아 전용 결제하기 누름')
            else:
                wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="결제하기"])[2]'))).click()  # 티맵
                print('티맵 전용 결제하기 누름')
    else:
        print('간편카드결제가 아니므로 결제하기 누르기')
        if who == 'carmore':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="결제하기"]'))).click()  # 카모아
            print('카모아 전용 결제하기 누름')
        else:
            wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="결제하기"])[2]'))).click()  # 티맵
            print('티맵 전용 결제하기 누름')
    print('안심플러스 금액 =', ansim_amount)
    return ansim_amount


def cancel_Process(wait,driver,scroll_wait,amount,what):
    down_swipe(driver)
    if what != 'month':
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        #안정적으로 하기 위해서.
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약취소"]'))).click()
    if what == 'month':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="월렌트 예약 취소"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"본인은 해당 월렌트 예약 취소 약관에 동의합니다.")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="확인"]'))).click()
    else:
        sleep(3)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약을 취소하시겠습니까?"]')))
        except:
            # 안눌렸을 때를 대비하여 다시 선택 하기
            down_swipe(driver)
            down_swipe(driver)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약취소"]'))).click()
        sleep(3)
        #예약취소화면
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약을 취소하시겠습니까?"]')))
    if what == 'hotel':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="호텔을 이용할 일정이 아예 취소 또는 연기되어서"]'))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="차량 배달 주소 변경"]'))).click()
    while_loop('//*[@text="간편카드결제"]', driver, 'down_find', 1500)
    while_loop('//*[contains(@text,"' + amount + '")]', driver, 'down_find', 2000)
    down_swipe(driver)
    down_swipe(driver)
    down_swipe(driver)
    down_swipe(driver)
    if what == 'hotel':
        while_loop('//*[@text="예약취소"]', driver, 'down_click', 2000)
    else:
        while_loop('//*[@text="예약 취소하기"]', driver, 'down_click', 2000)
    sleep(5)
    # 예약취소완료
    if what != 'hotel':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약취소 완료"]')))
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 취소 완료"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + amount + '")]')))
    down_swipe(driver)
    down_swipe(driver)
    down_swipe(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.Button[@text="확인"]'))).click()

def addOn(where,wait, driver, type,select):
    # 결제정보_추가옵션 영역, 추가 인원 선택 진행
    if type == 'hikari' or type == 'sicily':
        down_swipe(driver)
        down_swipe(driver)
        if where == '결제정보':
            while_loop('//*[contains(@text,"추가옵션(선택사항)")]', driver, 'down_click', 1800)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"추가 옵션은 예약과 함께 해당 렌트카 업체에 요청됩니다.")]')))
        else:
            # 차량상세 일 때
            while_loop('//*[@text="추가 옵션 정보"]', driver,'down_find', 1500)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"렌트카 업체에서 제공 가능한 옵션입니다.")]')))
        if type == 'hikari':
            if select == '토요타':
                while_loop('//*[contains(@text,"내비게이션")]', driver, 'down_click', 2000)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"무료")]')))
            elif select == '유럽카':
                # 유럽카일 때
                while_loop('//*[contains(@text,"카시트")]', driver, 'down_click', 2000)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"1개")]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"EUR")]')))
        elif type == 'sicily':
            while_loop('//*[contains(@text,"Baby seats")]', driver, 'down_click', 2000)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"EUR")]')))
            down_swipe(driver)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"대여기간 동안")]'))) # 아래쪽 추가 옵션으로 인식 안되는 경우 발생
        if where == '결제정보':
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="확인"]'))).click()  # 팝업 닫기
    else:
        #추가 옵션 없는 상품들
        pass

def freeCancel(now,startD,check,wait,m):
    start = now + timedelta(days=startD)
    check = start - timedelta(days=check)
    LA = start - timedelta(hours=17) #한국보다 17시간
    dateDict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="취소 수수료"]')))
    if m == 'm':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + str(check.year) + '년 ' + str(
            check.month) + '월 ' + str(check.day) + '일 (' + dateDict[check.weekday()] + ') 오후 12")]')))
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + str(check.year) + '년 ' + str(
            check.month) + '월 ' + str(check.day) + '일 (' + dateDict[check.weekday()] + ') 오전 10")]')))
    if m == 'LA':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"' + str(LA.year) + '년 ' + str(
            LA.month) + '월 ' + str(LA.day) + '일 (' + dateDict[LA.weekday()] + ') 오전 10")]')))


    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"무료 취소가 가능합니다.")]')))

def Cancel_table(wait,table):
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="대여시간"]')))
    if table == 'jeju':
        table = ["예약 후 1시간 이내", "100% 환불", "대여 72시간 이전", "100% 환불", "대여 72시간 전 ~ 48시간 전", "90% 환불",
             "대여 48시간 전 ~ 24시간 전", "80% 환불", "대여 24시간 전 ~ 1시간 전", "70% 환불", "1시간 미만", "50% 환불"]
    if table == 'seoul':
        table = ["예약 후 1시간 이내", "100% 환불", "대여 48시간 이전", "100% 환불", "대여 48시간 전 ~ 24시간 전", "90% 환불",
             "대여 24시간 전 ~ 1시간 전", "70% 환불", "1시간 미만", "50% 환불"]
    if table == 'month': #단기 15일 이상 ~ 월렌트
        table = ["예약 후 1시간 이내", "100% 환불", "대여 168시간 이전", "100% 환불", "대여 168시간 전 ~ 72시간 전", "90% 환불",
             "대여 72시간 전 ~ 24시간 전", "80% 환불", "24시간 미만", "70% 환불"]
    if table == 'guam':
        table = ["예약 후 1시간 이내", "100% 환불", "대여 72시간 이전", "100% 환불", "72시간 미만", "70% 환불"]
    if table == 'japan':
        table = ["예약 후 1시간 이내", "100% 환불", "대여 168시간 이전", "100% 환불", "대여 168시간 전 ~ 72시간 전", "80% 환불",
             "대여 72시간 전 ~ 24시간 전", "70% 환불", "24시간 미만", "50% 환불"]
    n = 2
    a = 0
    for i in range(0, int((len(table) / 2))):
        wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             '//android.widget.GridView/android.view.View[' + str(n) + ']/*[@text="' + table[a] + '"]')))
        wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             '//android.widget.GridView/android.view.View[' + str(n) + ']/*[@text="' + table[a + 1] + '"]')))
        n = n + 1  # 테이블 행
        a = a + 2  # 테이블 열
# str(today.year),  str(today.strftime('%m')) ,  str(today.strftime('%d'))
def select_Date(now,wait):
    today = now + timedelta(days=5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="'+str(today.strftime('%d'))+'"]'))).click()
    sleep(2)
    today2 = now + timedelta(days=6)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="' + str(today2.strftime('%d')) + '"]'))).click()
# # 임박예약 시의 최소 시간 계산 함수
# def min_time(now,day,type):
#     #timedelta(days=-3, hours=2, minutes=-10)
#     if type == 'jeju':
#         min_time = now + timedelta(minutes=+30) #30분 후의 시간을 구한다.
#         if min_time.strftime('%M') >= 30 : #만약 30분 후의 시간이 12시 31분이다.
#             #그럼 1시 30분 대여시간부터 노출 되어야 한다.
#             time() = hour()



# 해당 날짜의 요일을 계산하는 함수
def check_Date(now,day):
    today = now + timedelta(days=day)
    dateDict = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    month = today.month
    day = today.day
    weekday = dateDict[today.weekday()]
    year = today.year
    if today.day > 10:
        checkDate =str(today.month)+"."+str(today.day)+"("+dateDict[today.weekday()]+")"
        checkDate2 = str(today.month) + "." + str(today.day)
    else:
        checkDate = str(today.month) + ".0" + str(today.day) + "(" + dateDict[today.weekday()] + ")"
        checkDate2 = str(today.month) + ".0" + str(today.day)

    return checkDate,checkDate2

def down_swipe(driver):
    sleep(2)
    if username == 'joy':
        driver.swipe(300, 1000, 300, 500, 20)
    if username == 'levi':  # elif 추가 및 좌표 수정(levi)
        driver.swipe(300, 1000, 300, 800, 1000)
    sleep(2)

def short_swipe(driver):
    sleep(2)
    if username == 'joy':
        driver.swipe(300, 1500, 300, 1300, 20)
    if username == 'levi':  # elif 추가 및 좌표 수정(levi)
        driver.swipe(300, 1000, 300, 800, 1000)
    sleep(2)

def up_swipe(driver):
    sleep(2)
    if username == 'joy':
        driver.swipe(300, 800, 300, 1400, 40)
    elif username == 'levi':
        driver.swipe(300, 800, 300, 1000, 1000)  # down과 동일하게 수정(levi)
    sleep(2)


def while_loop(target,driver,what,line):
    wait = WebDriverWait(driver,5)
    num = 0
    while num < 10:
        try:
            y = wait.until(EC.element_to_be_clickable((By.XPATH, target))).location["y"]
            if y < line: #인식이 되어도 최소 높이만큼 올라와야 클릭 동작
                if what == 'down_click' or what == 'up_click':
                    wait.until(EC.element_to_be_clickable((By.XPATH, target))).click()
                else:
                    wait.until(EC.element_to_be_clickable((By.XPATH, target)))
                break
            else:
                if what == 'down_find' or what == 'down_click':
                    down_swipe(driver)
                else:
                    up_swipe(driver)
                num = num + 1
        except:
            #인식이 되지 않음
            if what == 'down_find' or what == 'down_click':
                down_swipe(driver)
            else:
                up_swipe(driver)
            num = num + 1

def change_type(want,wait):
    sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="최근 검색"]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("괌")
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"국가ㆍ괌")]'))).click()
    sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="괌"]')))
    if want == 'package':
        #패키지로 변환
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"운전자 연령")]')))  # 패키지 상태
        except:
            # 패키지 안되어 있는걸로 판단되어 패키지로 전환
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"함께 예약")]'))).click()  # 패키지 변환
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"운전자 연령")]')))
    else:
        # 단독으로 변환
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"운전자 연령")]')))  # 패키지 상태
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"함께 예약")]'))).click()  # 패키지 변환
        except:
            pass
def hotel_datePick(driver,wait):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="체크인 from-to 체크아웃"]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="일정 선택"]')))
        sleep(2)
        down_swipe(driver)
        down_swipe(driver)
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@text="28"])[2]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@text="29"])[2]'))).click()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="1박"]')))
        except:
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@text="28"])[2]'))).click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@text="29"])[2]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="1박"]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="적용하기"]'))).click()
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"1박")]')))
    except:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"1박")]')))
        print('날짜 선택 되어 있음')


def NaverPay(what,who,driver,wait):
    sleep(2)
    pay = '네이버페이'
    Payment(what,wait,who,pay)
    sleep(5)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카모아")]')))  # 결제 헤더가 있어서 결제 -> 카모아로 인식 단어 바꿈
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="네이버 앱으로 자동 로그인"]'))).click()
        sleep(3)
        try:
            if deviceID == '192.168.0.228:5555':
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="tmddh6023"]'))).click()
            else:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="joyto2"]'))).click()
            sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예"]'))).click()
            sleep(3)
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카모아")]')))
    if what == 'month':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"월렌트")]')))
    elif what == 'solo':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔모아")]')))
    elif what == 'package':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"패키지")]')))
    elif what == 'insurance':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"여행자 보험")]')))
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"단기렌트")]')))  # 월렌트 1개월도 생김
    if what == 'k_dev' or what == 'o_dev' or what =='h_dev':
        pass
    else:
        driver.back()
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
        except:
            pass

        driver.back()
        driver.back()
        driver.back()
        driver.back()
    print("Module-Naver pay 완료")

def KakaoPay(what,who,driver,wait):
    sleep(2)
    pay = '카카오페이'
    Payment(what, wait, who, pay)
    sleep(5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"다음")]')))
    driver.back()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 앱
    except:
        pass
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이 페이지 나가기"]'))).click()  # 웹 (티맵)
    except:
        pass
    driver.back()
    driver.back()

def SimpleCardPay(what,who,wait): #월렌트 2개월 이상 테스트에서는 사용하지 않는 모듈
    sleep(2)
    pay = '간편카드결제'
    ansim_amount = Payment(what, wait, who, pay)
    return ansim_amount


def CompanyCardPay(what,who,wait): # KTX 법인 카드 결제용 모듈
    sleep(2)
    pay = '간편카드결제'
    Payment(what, wait, who, pay)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"체크법인")]')))
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"결제하기")]'))).click()
    sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약 완료")]')))

def NormalPay(what,who,driver,wait): #신용/체크카드
    sleep(2)
    pay = '신용·체크카드'
    Payment(what, wait, who, pay)
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"NH pay(앱카드)")]')))
    driver.back()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 앱
    except:
        pass
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이 페이지 나가기"]'))).click()  # 웹 (티맵)
    except:
        pass
    driver.back()
    driver.back()

def TossPay(what,who,driver,wait):
    sleep(2)
    pay = '토스페이'
    Payment(what, wait, who, pay)
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"눌러주세요.")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]')))
    driver.back()
    driver.back()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 앱
    except:
        pass
    driver.back()
    driver.back()

def Account_Transfer(what,who,driver,wait):
    sleep(2)
    pay = '퀵계좌이체'
    Payment(what, wait, who, pay)
    sleep(2)
    # 토스페이먼츠 퀵계좌이체 화면으로 이동
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"계좌로")]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"퀵계좌")]'))) #퀵계좌결제 => 퀵계좌이체로 변경 예정 : 2024/1/3
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]')))
    sleep(3)
    driver.back()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 앱
    except:
        pass
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이 페이지 나가기"]'))).click()  # 웹 (티맵)
    except:
        pass
    driver.back()
    driver.back()
    driver.back()

def Insert_info(wait,driver):
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("자동화")
    sleep(2)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1021")]')))
    except:
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).click()
        sleep(3)
        birth = [16, 14, 8, 7, 9, 8, 66]  # 안드로이드 키패드 기준 : 971021 - 2 + 엔터(66)
        for i in range(0, len(birth), 1):
            driver.press_keycode(birth[i])
            sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1021")]')))  # 입력 확인
    sleep(2)
    down_swipe(driver)
    sleep(2)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="인증 완료"]')))
    except:
        print("이전 인증내역 풀림 확인 필요 / 인증 완료 텍스트 미 노출 ")
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[4]'))).send_keys("01082630856")
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="인증번호받기"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"발송되었습니다.")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="확인"])[2]'))).click() # 발송되었다는 안내 팝업 '확인' 클릭
        sleep(10)
        #자동입력되기를 기다리기
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click() # 확인 버튼 클릭
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"인증 되었")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 인증되었습니다 확인 팝업 선택
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="인증 완료"]')))

    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[5]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[5]'))).send_keys("joy@teamo2.kr")
    driver.back()
    sleep(2)

def Hotel_Insert_info(country,wait,driver,type):
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("AutoTest")
    sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).send_keys("CARMORE")
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="인증 완료"]')))
    except:
        print("이전 인증내역 풀림 확인 필요 / 인증 완료 텍스트 미 노출 ")
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[3]'))).send_keys("01082630856")
        sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="인증번호받기"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"발송되었습니다.")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="확인"])[2]'))).click() # 발송되었다는 안내 팝업 '확인' 클릭
        sleep(10)
        #자동입력되기를 기다리기
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click() # 확인 버튼 클릭
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"인증 되었")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()  # 인증되었습니다 확인 팝업 선택
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="인증 완료"]')))
    short_swipe(driver)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"@")]'))) #이메일 이미 입력되어 있는 상태
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText[@text=""])[1]'))).send_keys("joy@teamo2.kr")
    sleep(2)
    down_swipe(driver)
    sleep(2)
    if type == 'package':
        if country == 'overseas':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약자와 숙박자, 운전자 정보가 같습니다"]'))).click()
        else:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약자와 숙박자 정보가 같습니다"]'))).click()
        while_loop('//*[@text="이름"]', driver, 'down_find', 1500)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@hint="이름"]'))).send_keys("조이")
        except:
            pass
        sleep(2)
        try:
            while_loop('//*[@text="생년월일"]', driver, 'down_click', 1500)
            birth = [16, 14, 8, 7, 9, 8, 9]  # 안드로이드 키패드 기준 : 971021 - 2 + 엔터(66)
            for i in range(0, len(birth), 1):
                driver.press_keycode(birth[i])
                sleep(1)
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1021")]')))  # 입력 확인
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@hint="휴대폰 번호"]'))).send_keys("01082630856")
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="010-8263-0856"]')))
        except:
            pass
    else:
        while_loop('//*[contains(@text,"예약자와 숙박자 정보가 같습니다")]', driver, 'down_click', 1900)
    if country == 'overseas':
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="성별"])[2]'))).click()
        sleep(10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="여성"]'))).click()
    else:
        pass

def insurance_Insert_info(wait,driver,age,country):
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("조이")
    driver.press_keycode(66)
    sleep(2)
    if country == 'overseas':
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EdidtText)[2]'))).send_keys("SONG")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[3]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EdidtText)[3]'))).send_keys("JUNGEUN")
        driver.back()
    sleep(3)
    driver.press_keycode(66)
    if country == 'overseas':
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[4]'))).click()
    else:
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).click()
    if age == 27:
        birth = [8, 16, 16, 14, 8, 7, 9, 8,66]  # 안드로이드 키패드 기준 : 19971021 - 2 + 엔터(66)
        for i in range(0, len(birth), 1):
            driver.press_keycode(birth[i])
            sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1997")]')))  # 입력 확인
    # elif age == 18:
    #     birth = [8, 16, 16, 14, 8, 7, 9, 8, 66]  # 안드로이드 키패드 기준 : 19971021 - 2 + 엔터(66)
    #     for i in range(0, len(birth), 1):
    #         driver.press_keycode(birth[i])
    #         sleep(1)
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1997")]')))  # 입력 확인
    # elif age == 15:
    #     birth = [8, 16, 16, 14, 8, 7, 9, 8, 66]  # 안드로이드 키패드 기준 : 19971021 - 2 + 엔터(66)
    #     for i in range(0, len(birth), 1):
    #         driver.press_keycode(birth[i])
    #         sleep(1)
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1997")]')))  # 입력 확인
    # elif age == 80:
    #     birth = [8, 16, 16, 14, 8, 7, 9, 8, 66]  # 안드로이드 키패드 기준 : 19971021 - 2 + 엔터(66)
    #     for i in range(0, len(birth), 1):
    #         driver.press_keycode(birth[i])
    #         sleep(1)
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1997")]')))  # 입력 확인
    # else: # 100세
    #     birth = [8, 16, 16, 14, 8, 7, 9, 8, 66]  # 안드로이드 키패드 기준 : 19971021 - 2 + 엔터(66)
    #     for i in range(0, len(birth), 1):
    #         driver.press_keycode(birth[i])
    #         sleep(1)
    #     wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1997")]')))  # 입력 확인
    #     driver.back()

    driver.back()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="정보 입력 후 가격 확인"]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="1명, 24시간"]')))
    sleep(2)
    #성별 입력
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="성별"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.CheckedTextView[@text="여자"]'))).click()
    sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//android.view.View[@text="여자"]')))
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]'))).click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="대표자의 휴대폰 번호를 입력해 주세요"]')))
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
    if country == 'overseas':
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[5]'))).send_keys("01082630856")
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[3]'))).send_keys("01082630856")
    sleep(2)
    driver.press_keycode(66)
    driver.back()
    sleep(2)
    if country == 'overseas':
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[6]'))).send_keys("joy@teamo2.kr")
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[4]'))).send_keys("joy@teamo2.kr")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="joy@teamo2.kr"]')))
    driver.press_keycode(66)
    sleep(2)

def Cancel(wait,driver,type):
    down_swipe(driver)
    down_swipe(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 상세 내용 보기"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약 상세 정보")]')))
    reservation = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약번호")]'))).get_attribute(
        "text")
    sleep(3)
    if type == 'ktx':
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"예약이 확정되었습니다!")]')))
        for i in range(0, 5):
            down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"열차 운행 지연/중단 접수하기")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약 취소")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"취소하시는 이유는 어떻게 되시나요?")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"기타")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//android.widget.EditText'))).send_keys(
            'QA 자동화 테스트 취소 건 입니다.')
        driver.press_keycode(66)
        sleep(1)
        down_swipe(driver)
        down_swipe(driver)
        down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약취소")]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="예약 취소 완료"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"100% 환불")]')))
        print("100% 환불 처리됨")
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"역 -")]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"간편카드결제")]')))
        down_swipe(driver)
        down_swipe(driver)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
    return reservation

def Fail(title,num,reservation,driver):
    fail_msg = str(traceback.format_exc()).split('selenium.common.exceptions.TimeoutException')[0]
    file_path = '/Users/joy/Desktop/screenshot/Android_fail_'+str(now)+'.png'
    driver.save_screenshot(file_path)
    # screenshot = driver.get_screenshot_as_png()
    # pyautogui.screenshot().save('/Users/joy/Desktop/screenshot/fail'+str(now)+'.png')  # 파일로 저장
    if reservation == '':
        result_fail_msg = str(num) + '. ' + title + "______FAIL " + " : 확인 필요"+'\n'+"```"+str(fail_msg)+"```"
        result = str(num) + '. ' + title + " ______FAIL "
    else:
        result_fail_msg = str(num) + '. ' + title + "______FAIL" + " : 확인 필요" + '\n' + "```" + str(fail_msg) + "```"
        result = str(num) + '. ' + title + "______FAIL "
    slack_post_img(file_path,result_fail_msg)
    print(result_fail_msg)
    print('Fail 이미지 전송 완료',file_path)

def Pass(title,num,reservation):
    if reservation == '':
        result = str(num) + '. ' + title + " ______PASS"
    else:
        result = str(num) + '. ' + title + " ______PASS : " + reservation

    print(result)
    slack_post(result)

#정렬 변수
k_rolling ='인기순' # 차종순 -> 가격순 변경 시점 : 2023/11/17 -> 차종순 다시 변경 ^^ 2023/11/22 -> 인기순 변경 2024/7/16
j_rolling = '가격순'
o_rolling= '가격순'
m_rolling = '가격순'
