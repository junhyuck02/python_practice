"""
from extractors.wanted import extract_wanted_jobs
from file import save_to_file

keyword = input("What do you want to search for?")

jobs = extract_wanted_jobs(keyword)

save_to_file(keyword, jobs)
"""

from flask import Flask, render_template, request, redirect, send_file
from extractors.wanted import extract_wanted_jobs
from file import save_to_file

# flask는 html 파일을 templates라는 폴더에 저장해두고 사용함
# request는 사용자가 서버로 접속할 때 보내는 모든 정보를 담고 있음

app = Flask("JobScrapper")
# 어플리케이션의 이름을 설정하고 객체를 생성


@app.route("/")
# Decorator: 특정 url 경로로 접속했을 때 바로 밑에 작성한 함수를 실행해서 연결해줌
def home():
    return render_template("home.html")
    # 이 함수는 폴더 안의 html 파일을 찾아서 브라우저가 읽을 수 있는 형태로 변환해서 보내줌
    # html 내부에서 {{}}를 사용하면 변수를 전달해줄 수 있음


db = {}
# 가짜 db, 서버가 켜져있을때만 메모리에 있음
# 똑같은 검색어를 여러 번 검색할 때, 서버가 일을 덜 하게 만드는 효율적인 저장소(캐시라고함)


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    # request라는 객체 안에 있는 args라는 데이터 보관함에서 특정 값을 꺼내기
    if keyword == None:
        return redirect("/")
        # 홈화면으로 돌려보내기
    if keyword in db:
        # 내가 검색해본적 있니? 있으면 재사용
        jobs = db[keyword]
    else:
        jobs = extract_wanted_jobs(keyword)
        db[keyword] = jobs
        # 다음에 또 검색할 상황에 대비해 캐싱
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        # db에 있는지 확인하고 검색한적이 없어서 데이터가 없다면 검색 페이지로 보내버림
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)
    # send_file로 파일을 사용자의 컴퓨터로 보낸다
    # as_attachment=True: 웹 브라우저에서 파일을 바로 열려고 하지 않고, 다운로드 창을 띄워서 파일로 저장하게끔 함


app.run(debug=True)
# flask 어플리케이션을 실제로 시작하는 명령어
# debug=True: 코드를 수정하고 저장할 때마다 서버를 껐다 켤 필요 없이 자동으로 변경 사항이 반영됨
