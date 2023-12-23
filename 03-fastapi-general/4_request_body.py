# Request body?
# - path parameter, query parameter 는 URL 에 어떤 데이터가 전송되는지 보여진다. 이와 다르게 request body 의 정보는 감춰진다.
# - FastAPI 에서는 request body 를 만들기 위해 pydantic model 을 사용한다.
# - pydantic model 은 모델의 파싱과 validation 을 위한 라이브러리 이다.
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Pydantic model 을 사용하여 item 을 정의한다.
class Item(BaseModel):
    name: str
    description: str | None = None
    price: int


# Item 을 생성하는 POST method 라우터를 정의한다.
# endpoint name 에 plural 을 쓰는 것이 일반적이라고 함
# https://stackoverflow.com/questions/54057388/rest-api-resource-naming-conventions-user-or-users-pluralisation
@app.post("/items")
async def create_item(item: Item):
    # item attribute 에 직접 접근할 수도 있다.
    if item.description:
        item.description = item.description.upper()
    return item


# Request 에 path, body, query 를 모두 나타낼 수도 있다.
# - Pydantic model 을 쓰면 body 이다.
# - {item_num} 과 같이 중괄호로 사용되면 path param 이다.
# - Path param 도 아니고 pydantic model 도 아니면 query param 이다.
@app.post("/items/{item_id}")
async def create_item_with_id(item_id: int, item: Item, is_active: bool = True):
    # item_id; path param
    # item: request body
    # is_active: query param
    result = {"item_id": item_id, **item.model_dump()}
    return result


if __name__ == "__main__":
    uvicorn.run("4_request_body:app", host="localhost", port=8000, reload=True)
