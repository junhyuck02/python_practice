import requests
from bs4 import BeautifulSoup

all_jobs = []


def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("section", class_="jobs").find_all("li")[2:-1]
    # id는 그냥 하면 되지만 class로 검색하려면 class_로 해야함 파이썬에도 클래스가 있어서
    # find_all은 배열을 반환
    # [0:5] -> 이렇게 하면 인덱스 0 부터 인덱스 4까지 임
    # [1:] -> 이건 인덱스 1부터 끝까지
    # [1:-1] -> 이건 인덱스 1부터 인덱스 -2까지(뒤에서 두번째)
    # 구조 분해 할당 문법 가능
    # letters = ["a","b","c"] ---> a1,b1,c1 = letters

    EMPLOYMENT_TYPES = {"Full-Time", "Contract"}
    ignore_types = {"$", "USD", "Top 100", "Featured"}
    for job in jobs:
        title = job.find("span", class_="new-listing__header__title__text")
        company = job.find("p", class_="new-listing__company-name")

        categories = job.find_all("p", class_="new-listing__categories__category")
        employ_type = None
        region = []
        for category in categories:
            text = category.text.strip()
            # 앞 뒤 공백 정리
            if text in EMPLOYMENT_TYPES:
                employ_type = text
            elif text in ignore_types:
                continue
            else:
                region.append(text)
        url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
        # next_sibling은 찾은 값의 다음 요소를 달라는 것
        job_data = {
            "title": title.text,
            "company": company.text,
            "employ_type": employ_type,
            "region": ", ".join(region),
            "url": f"https://weworkremotely.com{url}",
        }
        all_jobs.append(job_data)


def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return len(soup.find("div", class_="pagination").find_all("span", class_="page"))


total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)


print(len(all_jobs))
