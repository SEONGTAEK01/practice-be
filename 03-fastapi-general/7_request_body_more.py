# 4_request_body.py 에서 query parameter 과 path parameter 를 같이 사용했다.
# 여기에 request body 를 추가한 예를 보자.
import uvicorn
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    description: str | None = None


class User(BaseModel):
    name: str
    address: str | None = None


app = FastAPI()

# query param, path param, request body 혼용의 예
# Path(), Query(), Body() class 를 명시적으로 넣는 것도 가독성에 괜찮아 보인다? 코드가 길어지긴 하지만.
@app.put("/items/{item_id}")
async def update_item(item_id: int = Path(..., title="업데이트를 위한 아이템 ID", ge=1, le=10),  # path param
                      q: str | None = Query(None, title="쿼리 파라미터"),  # query param
                      item: Item | None = Body(...)):  # request body
    # item_id 를 받아서 Item 형식으로 리턴한다.
    # q 가 존재하면 {"q": q} 를 리턴에 추가한다.
    # item 이 존재하면 request body 로 요청한 item 을 리턴에 추가한다.
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Request body 를 여러개 넣을 수도 있다.
@app.put("/multiple_bodies/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Body class 를 통한 단일값 선언
# - 위의 예제처럼 pydantic model 을 선언해서 request body 를 정의할 수도 있고, 인자에 Body() class 를 선언함으로써 body 를 정의할 수도 있다.
@app.put("/with_body_class/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: object = Body(...)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# 단일 request body 에 키 값 부여하기
# - FastAPI 에서는 request body 가 1개인 경우 키 값을 부여하지 않는다. 키 값을 부여하고 싶으면 Body() 에 embed=True option 을 준다.
# - Swagger 의 request body 부분에 키 값이 추가된 것을 볼 수 있다.
## embed=True
# {
#   "item": {
#     "name": "string",
#     "price": 0,
#     "description": "string"
#   }
# }
## embed=False
# {
#     "name": "string",
#     "price": 0,
#     "description": "string"
# }
@app.put("/with_embed_option/items/{item_id}")
async def update_item(item_id: int = Path(..., title="업데이트를 위한 아이템 ID", ge=1, le=10),  # path param
                      q: str | None = Query(None, title="쿼리 파라미터"),  # query param
                      item: Item | None = Body(..., embed=True)):  # request body
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


if __name__ == "__main__":
    uvicorn.run("7_request_body_more:app", host="localhost", port=8000, reload=True)
