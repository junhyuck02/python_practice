# 동기 방식의 api를 가져온다, 앞의 일이 끝날때까지 기다렸다가 다음 일을 한다는 말
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()
# 시동걸게

browser = p.chromium.launch(headless=False)
# 크롬 브라우저는 크로미움이라는 오픈소스 엔진을 기반으로 만들었음
# 크롬을 직접 켜는 것이 아니라, 자동화 테스트용으로 특수하게 만들어진 깨끗한 상태의 크롬 엔진을 실행
# headless를 False로 설정하면 브라우저 창을 실제로 화면에 띄움
# 위치 인수로 값을 할당하면 복잡할 때가 있음, 그래서 함수가 알고 있는 키워드 인수에 값을 할당하면 굳 (ex:headless)
# 싹 다 위치 인수로 하거나 싹 다 키워드 인수로 하는게 보편적임

# page.screenshot(path="screenshot.png")
# 스샷해서 사진으로 저장

page = browser.new_page()
# 새로운 페이지를 연다
"""
page.goto("https://www.wanted.co.kr/jobsfeed", wait_until="domcontentloaded")
# 해당 url로 이동, 완전 로딩까지 기다리지 말고 기본 골격만 뜨면 넘어가라

time.sleep(3)
# 3초 동안 코드 멈추기

page.click("button.wds-1cqc7gt")
# page.locator("button.wds-1cqc7gt").click() 이렇게 하는 방법도 있음

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# 입력창에 flutter라는 글자를 채워넣음

page.keyboard.press("Enter")
# 키보드에서 엔터 누르기

page.click("a#search_tab_position")

for x in range(2):
    page.keyboard.press("End")
    # 아래방향 키보드 누르기

content = page.content()
# html 소스를 전부 가져오기

input("엔터 누르면 종료...")
p.stop()
# 종료
"""

page.goto(
    "https://www.wanted.co.kr/search?query=flutter&tab=position",
    wait_until="domcontentloaded",
)
for x in range(2):
    time.sleep(2)
    page.keyboard.press("End")

time.sleep(5)

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all(
    "div", class_="JobCard_container__zQcZs JobCard_container--variant-card___dlv1"
)

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title___kfvj").text
    company_name = job.find(
        "span",
        class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6",
    ).text
    career = job.find(
        "span",
        class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6",
    ).text
    reward = job.find("span", class_="JobCard_reward__oCSIQ").text
    job = {
        "title": title,
        "company_name": company_name,
        "career": career,
        "reward": reward,
        "link": link,
    }
    jobs_db.append(job)

file = open("jobs.csv", "w")
# open은 파일을 열어주는 함수인데 해당 파일이 없으면 만들어주기도 함
# mode r은 read 수정 가능하게 하려면 write로
writer = csv.writer(file)
# 파일을 열고, 그 파일에 데이터를 행 단위로 써줌
writer.writerow(["Title", "Company Name", "Career", "Reward", "Link"])
# 한줄씩 데이터를 적는 함수
for job in jobs_db:
    writer.writerow(job.values())
    # dicts에는 keys(), values() 메소드가 있음

file.close()
