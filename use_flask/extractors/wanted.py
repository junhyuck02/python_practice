from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


class WantedJobScrapper:
    # 데이터를 수집하는 로봇
    def __init__(self):
        # 초기화
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.keywords = []
        self.result = []

    def add_keyword(self, keyword):
        # 무엇을 검색할지 정해준다
        if isinstance(keyword, list) == True:
            # isinstance는 이 데이터가 내가 원하는 타입이 맞는지 검사하는 함수
            self.keywords = keyword
            # 리스트라면 기존 리스트에서 새로 받은 리스트 전체로 바꿔끼운다
        elif isinstance(keyword, str) == True:
            self.keywords.append(keyword)
            # 문자열이라면 기존에 있던 리스트에 단어를 추가
        print(f"Keywords : {self.keywords}")

    def reset(self):
        # 뒷정리
        self.keywords.clear()
        self.p.stop()

    def start(self):
        # 사이트에서 데이터를 긁어온다
        for keyword in self.keywords:
            print(f"Scrapper {keyword}...")
            page = self.browser.new_page()
            page.goto(
                f"https://www.wanted.co.kr/search?query={keyword}&tab=position",
                wait_until="domcontentloaded",
            )

            for x in range(5):
                time.sleep(5)
                page.keyboard.press("End")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find_all(
                "div",
                class_="JobCard_container__zQcZs JobCard_container--variant-card___dlv1",
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

            self.result = jobs_db
        self.reset()

        return self.result


def extract_wanted_jobs(keyword):
    scrapper = WantedJobScrapper()
    scrapper.add_keyword(keyword)
    return scrapper.start()
