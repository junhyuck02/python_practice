"""
from extractors.wanted import extract_wanted_jobs
from file import save_to_file

keyword = input("What do you want to search for?")

jobs = extract_wanted_jobs(keyword)

save_to_file(keyword, jobs)
"""

from flask import Flask

app = Flask("JobScrapper")
# 어플리케이션의 이름을 설정하고 객체를 생성


@app.route("/")
# Decorator: 특정 url 경로로 접속했을 때 바로 밑에 작성한 함수를 실행해서 연결해줌
def home():
    return "Hello! Welcome to Job Scrapper!"


app.run(debug=True)
# flask 어플리케이션을 실제로 시작하는 명령어
# debug=True: 코드를 수정하고 저장할 때마다 서버를 껐다 켤 필요 없이 자동으로 변경 사항이 반영됨
