"""
파이썬의 자료구조

다른 언어와 달리 인덱스를 -1 -2 .. 로 하면 뒤에서부터 접근 가능
리스트와 튜플 모두 적용됨, dicts는 안됨
1. list: 걍 배열임
count, clear, reverse, append, remove

2. tuple: list와 달리 () 사용, 튜플 내의 요소 삽입, 삭제가 불가능
count, index

3. dictionary: map과 같이 key와 value가 있음
    
    Dicts = {
    "name": "nico",
    "age": 12,
    "alive": True
    }
    값을 가져오려면 Dicts.get(key)를 하거나 Dicts["key"]를 하면 됨
    값을 지우려면 pop, 추가하려면 Dicts["key"] = value 하면 됨
    딕셔너리 안에서의 튜플은 내용을 통째로 다른걸로 대체시킬수 있으나 역시 추가나 삭제는 안됨
--------------------------------------------------------------------------------

기본 라이브러리 말고 다른 사람이 만든 모듈을 쓰고 싶으면 pypi ㄱㄱ



"""