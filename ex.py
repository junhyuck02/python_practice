from requests import get
# pypi에서 설치한 requests는 파이썬 코드에서 웹사이트로 요청 전송을 가능하게 함

websites = (
    "google.com",
    "naver.com",
    "https://airbnb.com",
    "facebook.com",
    "https://tiktok.com"
)

results = {}

for i in websites:
    if not i.startswith("https://"):
        i = f"https://{i}"
    
    response = get(i)
    # get은 웹사이트의 응답을 반환해줌
    if response.status_code == 200:
        print(f"{i} is ok")
        results[i] = "OK"
    else:
        print(f"{i} not ok")
        results[i] = "FAILED"

print(results)