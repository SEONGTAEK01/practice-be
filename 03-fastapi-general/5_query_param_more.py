# 'Query' class 를 사용해서 query param 을 좀 더 깊이 다뤄보자.
# 'Query' class 를 사용하면 min, max length 제한을 걸 수 있는 등 좀 더 다양한 기능을 사용할 수 있다.

import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()


# 'query_param' 을 10자로 제한 해보자.
@app.get("/items")
async def read_items(query_param: str = Query(None, max_length=10)):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


# 'query_param' 을 3-10자로 제한 해보자.
@app.get("/items")
async def read_items(query_param: str = Query(None, min_length=3, max_length=10)):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


# 'query_param' 에 특정한 값만 올 수 있게 제한해보자. (정규식 사용 가능!)
# -'prefixed' 라는 값만 'query_param' 에 올 수 있다.
@app.get("/items")
async def read_items(query_param: str = Query(None, min_length=3, max_length=10, regex="^prefixed$")):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


# 'query_param' 을 required field 로 만들어 보자.
# - '...' 을 default value 로 주면 된다.
@app.get("/items")
async def read_items(query_param: str = Query(..., min_length=3, max_length=10, regex="^prefixed$")):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


# 'query_param' 으로 리스트 받기
# - 리스트로 default 값을 줄 수도 있다.
@app.get("/items/list")
async def read_list_items(query_param: list[str] = Query(default=['foo', 'bar'])):
    results = {"query_param": query_param}
    return results


# 3.5 에서 도입되었던 타입힌트가 3.9 부터 사라짐.
# - TypeHint 모듈을 따로 import 해야하고, built-in 자료형 이름과 같은 기능을 하는데 2가지 방법이 있으므로 consistency 가 떨어지기 때문이다.
#   앞으로 그냥 built-in typing 을 쓰자!

# metadata 추가하기
@app.get("/items")
async def read_items_metadata_test(query_param: str = Query(None, title="Title", description="쿼리 스트링 설명")):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


# alias 추가하기
# - 원래 'item-query' 는 파이썬에서 변수로 쓸 수 없다. 하지만 'alias' 를 통해 'item-query' 로 리퀘스트를 보낼 수 있게 만든다.
# curl -X 'GET' \
#   'http://localhost:8000/items?item-query=1' \
#   -H 'accept: application/json'

# * 'title' 은 '/redoc' 에서 쓰인다. Swagger 에서는 'description' 을 사용한다.
@app.get("/items")
async def read_items_metadata_test(
        query_param: str = Query(None, title="Title", description="쿼리 스트링 설명", alias="item-query", deprecated=True)):
    results = {"items": [{"id": "foo"}, {"id": "bar"}]}
    if query_param:
        results.update({"query_param": query_param})
    return results


if __name__ == "__main__":
    uvicorn.run("5_query_param_more:app", host="localhost", port=8000, reload=True)
