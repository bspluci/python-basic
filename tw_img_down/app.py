from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import os

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 로그인 정보
username = ""  # 트위터 사용자 이름
id = ""  # 트위터 아이디
password = ""  # 트위터 비밀번호

try:
    # 트위터 로그인 페이지 열기
    driver.get("https://x.com/i/flow/login")

    # 로그인 폼이 로드될 때까지 대기
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "text"))
    )
    driver.find_element(By.NAME, "text").send_keys(username)
    driver.find_element(By.NAME, "text").send_keys(Keys.RETURN)

    # 아이디 입력 대기
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "text"))
    )
    driver.find_element(By.NAME, "text").send_keys(id)
    driver.find_element(By.NAME, "text").send_keys(Keys.RETURN)

    # 비밀번호 입력 대기
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # 로그인 완료 대기
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(5)  # 추가 대기 시간 (필요에 따라 조정)

    for _ in range(3):  # 3번 스크롤 (필요에 따라 조정)
        WebDriverWait(driver, 200).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "img.css-9pa8cd[alt='Image']")
            )
        )

        time.sleep(2)  # 추가 대기 시간 (필요에 따라 조정)

        # 이미지 태그의 src 가져오기
        images = driver.find_elements(
            By.CSS_SELECTOR, "img.css-9pa8cd[alt='Image']"
        )
        image_folder = "./twitter/images"
        os.makedirs(image_folder, exist_ok=True)

        for img in images:
            img_url = img.get_attribute("src")
            if img_url:
                # 이미지 다운로드
                img_data = requests.get(img_url).content
                img_name = os.path.join(
                    image_folder, img_url.split("/")[-1] + ".jpg"
                )  # 이미지 파일 이름 생성
                with open(img_name, "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded {img_name}")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(5)  # 페이지 로드 대기

finally:
    # 웹 드라이버 종료
    print("작업이 완료되었습니다.")
    # driver.quit()  # 브라우저를 닫지 않으려면 이 줄을 주석 처리합니다.

# 이 줄을 추가하여 사용자가 종료할 때까지 대기합니다.
input("브라우저를 종료하려면 Enter 키를 누르세요.")
