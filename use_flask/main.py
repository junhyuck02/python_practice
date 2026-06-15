"""
from extractors.wanted import extract_wanted_jobs
from file import save_to_file

keyword = input("What do you want to search for?")

jobs = extract_wanted_jobs(keyword)

save_to_file(keyword, jobs)
"""

from flask import Flask, render_template

# flask는 html 파일을 templates라는 폴더에 저장해두고 사용함

app = Flask("JobScrapper")
# 어플리케이션의 이름을 설정하고 객체를 생성


@app.route("/")
# Decorator: 특정 url 경로로 접속했을 때 바로 밑에 작성한 함수를 실행해서 연결해줌
def home():
    return render_template("home.html", name="jj")
    # 이 함수는 폴더 안의 html 파일을 찾아서 브라우저가 읽을 수 있는 형태로 변환해서 보내줌
    # html 내부에서 {{}}를 사용하면 변수를 전달해줄 수 있음


@app.route("/search")
def hello():
    return "hello"


app.run(debug=True)
# flask 어플리케이션을 실제로 시작하는 명령어
# debug=True: 코드를 수정하고 저장할 때마다 서버를 껐다 켤 필요 없이 자동으로 변경 사항이 반영됨
