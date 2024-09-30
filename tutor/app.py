from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 로그인 정보
j_username = "tutoring51"
j_password = "rhdrhdclf0"

posts = []

try:
    driver.get("https://stgtutoring.ebsoc.co.kr/member/login")

    # 로그인 폼이 로드될 때까지 대기
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "j_username"))
    )
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "j_password"))
    )
    driver.find_element(By.NAME, "j_username").send_keys(j_username)
    driver.find_element(By.NAME, "j_password").send_keys(j_password)
    driver.find_element(By.NAME, "j_password").send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )

    driver.get("https://stgtutoring.ebsoc.co.kr/cs/notice")

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.board-table__anchor")
        )
    )

    list_items = driver.find_elements(By.CSS_SELECTOR, "a.board-table__anchor")

    for i, item in enumerate(list_items):
        # 목록을 다시 가져와야 stale element reference 예외를 피할 수 있습니다.
        list_items = driver.find_elements(
            By.CSS_SELECTOR, "a.board-table__anchor"
        )
        item = list_items[i]

        driver.execute_script(
            "arguments[0].dispatchEvent(new MouseEvent('click', "
            "{bubbles: true, cancelable: true, view: window}));",
            item,
        )

        try:
            title_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".notice-page__head--title")
                )
            )
            WebDriverWait(driver, 20).until(
                lambda driver: driver.execute_script(
                    'return arguments[0].innerText.trim() !== "";',
                    title_element,
                )
            )
            title = title_element.text

            date_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".notice-page__head--date span:nth-child(2)",
                    )
                )
            )
            WebDriverWait(driver, 20).until(
                lambda driver: driver.execute_script(
                    'return arguments[0].innerText.trim() !== "";',
                    date_element,
                )
            )
            date = date_element.text

            content_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".notice-page__content")
                )
            )
            content = (
                content_element.text.replace("\n", "\\n")
                if content_element.text.strip()
                else "내용 없음"
            )

            posts.append({"title": title, "date": date, "content": content})

        except (TimeoutException, NoSuchElementException) as e:
            print(f"해당 페이지의 요소를 찾을 수 없습니다: {e}")
            posts.append(
                {
                    "title": title if "title" in locals() else "제목 없음",
                    "date": date if "date" in locals() else "날짜 없음",
                    "content": "내용 없음",
                }
            )

        driver.back()

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.board-table__anchor")
            )
        )
finally:
    # 파일을 'w' 모드로 열어 기존 내용을 덮어씁니다.
    with open("./tutor/notice.csv", "w", encoding="utf-8-sig") as file:
        file.write("제목, 날짜, 내용\n")
        for post in posts:
            file.write(f'{post["title"]}, {post["date"]}, {post["content"]}\n')

    # 웹 드라이버 종료
    print("작업이 완료되었습니다.")
    # driver.quit()  # 브라우저를 닫지 않으려면 이 줄을 주석 처리합니다.

# 이 줄을 추가하여 사용자가 종료할 때까지 대기합니다.
input("브라우저를 종료하려면 Enter 키를 누르세요.")
