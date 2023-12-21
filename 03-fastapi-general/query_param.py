from typing import Optional

import uvicorn
from fastapi import FastAPI

fake_db = [{"item_name": "espresso"}, {"item_name": "caffe latte"}, {"item_name": "americano"}]

app = FastAPI()


# Path parameter 에 없는 파라미터를 쿼리 파라미터라고 한다.
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


# bool 로 선언해 놓으면 아래 쿼리파라미터가 알아서 'True' 로 타입 컨버전 된다.
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


if __name__ == "__main__":
    uvicorn.run("query_param:app", host="localhost", port=8000, reload=True)
