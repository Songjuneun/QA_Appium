from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from datetime import *

# Desired Capabilities 설정
import Module
now = datetime.now()
# Connect to Appium server on local host
driver = webdriver.Remote('http://localhost:4723', Module.Setting_Reset('no'))


def find_image_on_screen(driver, template_path, threshold=0.8):
    # 화면 스크린샷 가져오기
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 템플릿 이미지 로드
    template = cv2.imread(template_path, 0)

    # 스크린샷을 그레이스케일로 변환
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 템플릿 매칭
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 매칭된 위치 확인
    if max_val >= threshold:
        return max_loc
    else:
        return None


try:
    # 이미지 매칭을 통해 비밀번호 4번 위치 찾기
    password_field_position_1 = find_image_on_screen(driver, '/Users/joy/Downloads/1.jpeg')
    password_field_position_7 = find_image_on_screen(driver, '/Users/joy/Downloads/7.jpeg')

    x1, y1 = password_field_position_1
    x7, y7 = password_field_position_7

    # 비밀번호 필드 클릭 (중심 클릭)
    password_field_size_1 = Image.open('/Users/joy/Downloads/1.jpeg').size
    driver.tap([(x1 + password_field_size_1[0] // 2, y1 + password_field_size_1[1] // 2)])
    password_field_size_7 = Image.open('/Users/joy/Downloads/7.jpeg').size
    driver.tap([(x7 + password_field_size_7[0] // 2, y7 + password_field_size_7[1] // 2)])
    password_field_size_1 = Image.open('/Users/joy/Downloads/1.jpeg').size
    driver.tap([(x1 + password_field_size_1[0] // 2, y1 + password_field_size_1[1] // 2)])
    password_field_size_7 = Image.open('/Users/joy/Downloads/7.jpeg').size
    driver.tap([(x7 + password_field_size_7[0] // 2, y7 + password_field_size_7[1] // 2)])
    password_field_size_1 = Image.open('/Users/joy/Downloads/1.jpeg').size
    driver.tap([(x1 + password_field_size_1[0] // 2, y1 + password_field_size_1[1] // 2)])
    password_field_size_7 = Image.open('/Users/joy/Downloads/7.jpeg').size
    driver.tap([(x7 + password_field_size_7[0] // 2, y7 + password_field_size_7[1] // 2)])


finally:
    # 테스트가 끝나면 드라이버 종료
    driver.quit()
