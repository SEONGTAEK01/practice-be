from typing import Optional

import uvicorn
from fastapi import FastAPI

fake_db = [{"item_name": "espresso"}, {"item_name": "caffe latte"}, {"item_name": "americano"}]

app = FastAPI()


# Path parameter 에 없는 파라미터를 query string 한다.
# 아래에선 'skip', 'limit' 이 쿼리 파라미터다.
# 타입을 명시하지 않으면 문자열로 간주한다. API 작성할 때는 무조건 타입을 명시하자. TypeScript 처럼!
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    # async def read_items(skip = 0, limit: int = 10):
    return fake_db[skip: skip + limit]


# 생략가능한 파라미터를 만들고 싶으면 'Optional' 을 쓴다. 또는 '|' 를 쓴다.
@app.get("/items/optional_test")
async def read_items_optional(x: int = 3, y: Optional[int] = None):
    if y:
        return x + y
    return x


# Query string 을 required 하게 만들려면? -> 아무값도 넣지 않으면 된다.
# - Optional 을 뺀다.
# - default value 를 지정하지 않는다.
@app.get("/items/{user_id}")
async def read_items_with_user_id(user_id: int, upper_case: bool = False):  # upper_case 가 required field 가 아니다.
# async def read_items_with_user_id(user_id: int, upper_case: bool): # upper_case 가 required field 이다.
    # user_id 에 해당하는 user 가 존재하면 해당 아이템을 리턴한다.
    # upper_case 가 true 이면 name 을 대문자로 바꾼다.
    fake_db = {1: {"name": "seongtaek"}}

    user = fake_db.get(user_id)
    if user:
        if upper_case:
            upper_cased_user = { k.upper(): v.upper() for k, v in user.items()}
            return upper_cased_user
        else:
            return user


# bool 로 선언해 놓으면 아래 query string 이 알아서 'True' 로 타입 컨버전 된다.
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=true
@app.get("/items/type_conversion/{item_id}")
async def read_item_type_conversion(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# <query string and path parameter 는 뭐가 다른거야?>
# 레퍼런스: https://velog.io/@juno97/API-Path-parameter-VS-Query-Parameter-%EA%B8%B0%EB%A1%9D%EC%9A%A9
# path param
# - 특정한 하나의 목적으로 API 를 호출할 때 사용한다. 정확하게 정해진 특정한 목적을 표현할 때 사용한다.
# - 예를 들어, http://www.naver.com/stocks/{company_number} [GET] 이라는 API 가 있다고 하면, 이 API 는 company_name 으로
# - 현재 주식을 가져오라는 것을 명확히 표현하는 API 인 것이다.
#
# query string
# - 이름부터 query 이고, 'string' 이다. 어떤 질문을 할 것인데 이것이 'string' 형태로 서버에 전달되는 형태이다.
# - path param 과의 가장 큰 차이점은 '조건' 을 가진다는 것이다. path param 에서는 '32455' 이라는 주식번호를 가진 것을 가져와라!
#   라고 1가지 내용의 요청만 할 수 있지만, query string 에서는 '조건' 을 줄 수 있다는 점이 가장 큰 차이점이다.
# - 예를들어 stock id 가 '32455' 이고 2023-01 월부터 2023-06 월 까지의 가격을 불러와 줘! 라고 한다면 이는 path param 으로 요청하기가 어렵다.
# - 하지만 query string 으로는 가능하다. http://www.naver.com/{stock_id}/?start_date=202301&end_date=202306 의 query string
#   형태의 API 를 만들면 된다.
#
# 자주 사용되는 곳
# - 필터 / 서치 / 정렬 / Pagination

if __name__ == "__main__":
    uvicorn.run("query_param:app", host="localhost", port=8000, reload=True)
