
from time import *
import getpass
import traceback
from slacker import Slacker
from datetime import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction

username = getpass.getuser()
carmore_store = '/Users/' + username + '/Downloads/렌트카 카모아 - 국내 해외 렌터카 1등_4.1.29_Apkpure.apk'
carmore_test = '/Users/' + username + '/Downloads/dev_carmore_4.1.36.apk'
tmap ='/Users/' + username + '/Downloads/TMAP  10.0.0.291979.apk'

if username == 'joy':
    # Galaxy S23+
    deviceID = '192.168.1.5:5555'
    platformVersion = '14'
    deviceName = 'S23+'
elif username == 'levi': #elif를 통해 levi 추가(levi)
     deviceID = '192.168.1.4:5555'
     platformVersion = '13'
     deviceName = 'S23'
else:
    deviceID = '192.168.0.228:5555'

def slack_post(result):
    slack = Slacker('{API 키}')
    slack.chat.post_message('#{슬랙 채널명}', str(result), '{스레드명}', None, None, None, None, None,None, None, ':100-billion:')

def server(wait):
    sleep(2)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="실서버"]'))).click()
        sleep(1)
        wait.until(EC.presence_of_element_located((By.ID, 'android:id/button1'))).click()
        sleep(3)
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))

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

def login(wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"카카오톡으로 로그인")]'))).click()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"즐거운 여정 시작하기")]'))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="닫기"]'))).click()
    print("실서버 Module-login 완료")

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
        sleep(4)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="로그아웃"]'))).click()
        sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
        sleep(5)
        server(wait)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@text="홈"]')))
    print("Module-logout 완료")

def exception(driver,wait):
    driver.terminate_app('com.gogocarhome.gogocar')
    driver.activate_app('com.gogocarhome.gogocar')
    sleep(5)
    server(wait)
    try:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"홈")]'))).click()
        except:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="허용"]'))).click()
            except:
                pass
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="모든 권한 허용하기"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="앱 사용 중에만 허용"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="허용"]'))).click()  # 4.1.28 부터 생김
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@text="허용"]'))).click()  # 알림 허용
            except:
                pass
            sleep(5)
            TouchAction(driver).tap(x=532, y=1971).perform()  # 시작하기 버튼 클릭
            sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
        try:
            logout(driver,wait)
        except:
            pass
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="홈"]'))).click()

    print("Module-exception 완료")

def L_exception(driver,wait):

    driver.terminate_app('com.gogocarhome.gogocar')
    driver.activate_app('com.gogocarhome.gogocar')
    sleep(5)
    server(wait)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
    print("app restart")
    sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"My")]'))).click()
    sleep(5)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"예약내역")]')))
    except:
        wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@text="가입 / 로그인 하기"]'))).click()
        login(wait)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]'))).click()
    print("Module-L-exception 완료")

def T_exception(driver,wait):
    driver.terminate_app('com.skt.tmap.ku')
    driver.activate_app('com.skt.tmap.ku')
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="렌터카"]'))).click()
    except:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"업데이트")]')))
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="닫기"]'))).click()  # 개발섭이라 노출되는 팝업
    # try:
    #     wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"오늘은 그만보기")]'))).click()# 두번 노출될 가능성 있음.
    # except:
    #     pass
    # # 렌터카 클릭하기
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="렌터카"]'))).click()
    sleep(5)
    # 카모아 진입 확인
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"단기렌트")]')))
    print("Module-T-exception 완료")

def hotel_Coupon(where, amount,wait):
    coupon_available ='yes'
    if where == '제주' and amount >= 100000 and amount < 200000:
        coupon = '3,000'
    elif where == '제주' and amount >= 200000:
        coupon = '7,000'
    elif where == '내륙' and amount >= 150000 and amount < 500000:
        coupon = '6,000'
    elif where == '내륙' and amount >= 500000:
        coupon = '20,000'
    elif where == '해외' and amount >= 150000:
        coupon = '7,000'
    elif where == '해외' and amount >= 400000:
        coupon = '15,000'
    else:
        coupon_available ='no'
        coupon =0

    if coupon_available =='yes':
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@text,"3초 가입하고 ' + str(coupon) + '원 할인받기!")]')))
    else:
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
def select_Date(now,day):
    today = now + timedelta(days=day)
    selecttoday = str(today.year) + "-" + str(today.strftime('%m')) + "-" + str(today.strftime('%d'))

    return selecttoday

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
        driver.swipe(300, 1500, 300, 1000, 20)
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


def while_loop(self,target,driver,scroll_wait,what,line):
    num = 0
    if what == 'down_find' or what == 'down_click':
        sleep(2)
        while True:
            try:
                if num > 10:
                    break
                else:
                    y = scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target))).location["y"]
                    if y < line:
                        if what == 'down_click':
                            scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target))).click()
                        else:
                            scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target)))
                        break
                    else:
                        self.assertEqual(0, 1)
            except:
                down_swipe(driver)
                num = num+1
    elif what == 'up_find' or what == 'up_click':
        sleep(2)
        while True:
            num=num+1
            try:
                if num > 10:
                    break
                else:
                    y = scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target))).location["y"]
                    if y > line:
                        if what == 'up_click':
                            scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target))).click()
                        else:
                            scroll_wait.until(EC.element_to_be_clickable((By.XPATH, target)))
                        break
                    else:
                        self.assertEqual(0, 1)
            except:
                up_swipe(driver)
                num = num + 1

def while_click_back(target,driver,scroll_wait):
    count = 0
    while True:
        try:
            scroll_wait.until(EC.presence_of_element_located((By.XPATH, target))).click()
            break
        except:
            driver.back()
            driver.back()
            driver.back()
            count = count+1
        if count == 5:
            break

def Payment(what,wait,who,pay):
    #what = 'ktx','jeju','k_short', 'month', 'overseas'
    if what == 'jeju' or what == 'k_short' or what == 'month' or what == 'hotel':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"결제하기")]'))).click() #단기렌트, 월렌트
    elif what == 'o_short_direct' or what == 'o_short_api':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예약하기")]'))).click() #해외렌트
    elif what == 'insurance':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]'))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"예매하기")]'))).click() #ktx
    sleep(3)
    if what == 'jeju':
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="혜택 받지 않기"]'))).click() #정형화되었을 때 뜨는 팝업 (제주 리본/파트너스 , 내륙 아직 미적용)
        except:
            print("정형화 되지 않은 업체 입니다 -> 확인 필요")
    else:
        pass
    if what == 'o_short_direct' or what == 'o_short_api':
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click() #운전자 나이로 인한 가격 변동
            print("가격 변동 있음")
        except:
            print("가격 변동 없음")
    else:
        pass
    # 최종 결제 확인 모달 결제하기 클릭ㅈ
    if what == 'insurance':
        pass
    else:
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
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="농협"]'))).click()
    if pay == '간편카드결제':
        pass
    else:
        if who == 'carmore':
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="결제하기"]'))).click()  # 카모아
        else:
            wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@text="결제하기"])[2]'))).click() #티맵
    sleep(3)

def firstStart(wait):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="홈"]')))
    except:
        server(wait)

def NaverPay(what,who,driver,wait):
    sleep(2)
    pay = '네이버페이'
    Payment(what,wait,who,pay)
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
    elif what == 'hotel':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"호텔모아")]')))
    elif what == 'insurance':
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"여행자 보험")]')))
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"단기렌트")]')))  # 월렌트 1개월도 생김
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
    print("Module-Naver pay 완료")

def KakaoPay(what,who,driver,wait):
    sleep(2)
    pay = '카카오페이'
    Payment(what, wait, who, pay)
    sleep(5)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]')))
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
    Payment(what, wait, who, pay)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="일시불"]')))

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
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="이 페이지 나가기"]'))).click()  # 웹 (티맵)
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
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("팀오투테스트_자동화")
    sleep(2)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"102s1")]')))
    except:
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).click()
        sleep(3)
        # List Of Key codes:
        # a - z-> 29 - 54
        # "0" - "9"-> 7 - 16
        # BACK BUTTON - 4, MENU BUTTON - 82
        # UP-19, DOWN-20, LEFT-21, RIGHT-22
        # SELECT (MIDDLE) BUTTON - 23
        # SPACE - 62, SHIFT - 59, ENTER - 66, BACKSPACE - 67
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
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[4]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[4]'))).send_keys("joy@teamo2.kr")
    driver.back()
    sleep(2)

def Hotel_Insert_info(self,wait,driver,type):
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
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@text="joy@teamo2.kr"]')))
    except:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText[@text=""])[1]'))).send_keys("joy@teamo2.kr")
    sleep(3)
    while_loop(self,'//*[contains(@text,"예약자와 숙박자 정보가 같습니다")]', driver, wait, 'down_click', 1900)
    if type == 'package':
        while_loop(self,'//*[contains(@text,"운전자 정보")]', driver, wait, 'down_click', 1500)
        sleep(2)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@hint="이름"]'))).send_keys("팀오투테스트_자동화")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="생년월일"]'))).click()
            birth = [16, 14, 8, 7, 9, 8, 9, 66]  # 안드로이드 키패드 기준 : 971021 - 2 + 엔터(66)
            for i in range(0, len(birth), 1):
                driver.press_keycode(birth[i])
                sleep(1)
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@text,"1021")]')))  # 입력 확인
            # down_swipe(driver)
            # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@hint="휴대폰번호"]'))).send_keys("01082630856")
            driver.back()
        except:
            pass
def insurance_Insert_info(wait,driver,age,country):
    wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[1]'))).send_keys("자동화테스트")
    sleep(2)
    if country == 'overseas':
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[2]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EdidtText)[2]'))).send_keys("SONG")
        sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EditText)[3]'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.EdidtText)[3]'))).send_keys("JUNGEUN")
        driver.back()
    sleep(3)
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
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="540원"]')))
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="다음"]'))).click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="대표자의 휴대폰 번호를 입력해 주세요"]')))
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="확인"]'))).click()
    if country == 'overseas':
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[5]'))).send_keys("01082630856")
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[3]'))).send_keys("01082630856")
    sleep(2)
    driver.back()
    sleep(2)
    if country == 'overseas':
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[6]'))).send_keys("joy@teamo2.kr")
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '(//android.widget.EditText)[4]'))).send_keys("joy@teamo2.kr")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@text="joy@teamo2.kr"]')))
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

def Fail(title,num,reservation):
    fail_msg = traceback.format_exc()
    if reservation == '':
        result_fail_msg = str(num) + '. ' + title + " [ FAIL ]" + " : 확인 필요"+'\n'+"```"+str(fail_msg)+"```"
        result = str(num) + '. ' + title + " [ FAIL ]"
    else:
        result_fail_msg = str(num) + '. ' + title + " [ FAIL ]" + " : 확인 필요" + '\n' + "```" + str(fail_msg) + "```"
        result = str(num) + '. ' + title + " [ FAIL ]"
    print(result)
    slack_post(result_fail_msg)

def Pass(title,num,reservation):
    if reservation == '':
        result = str(num) + '. ' + title + " [ PASS ]"
    else:
        result = str(num) + '. ' + title + " [ PASS ] : " + reservation

    print(result)
    slack_post(result)

#정렬 변수
k_rolling ='차종순' #차종순 -> 가격순 변경 시점 : 2023/11/17 -> 차종순 다시 변경 ^^ 2023/11/22
j_rolling = '가격순'
o_rolling= '가격순'
m_rolling = '가격순'

