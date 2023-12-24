# <Response Model>
# - API 의 response model 을 지정해 줄 수 있다.
# - doc 시스템에 설명이 추가되는 것도 장점이지만 가장 중요한 점은 output model 을 지정한 모델로만 out 되게 할 수 있다는 점이다.
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class User(BaseModel):
    id: str
    password: str
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    city: str = "Seoul"


# 회원가입을 예시로 테스트 해보자.
# - password 를 response 할 필요 없으므로 UserResponse 를 만들고 password 를 제거한다.
@app.post("/users", response_model=UserResponse)
async def create_user(user: User):
    return user


# fake items
items = {
    "hong": {"id": "sabitz", "name": "seongtaek", "email": "hongseongtaek@gmail.com"},
    "you": {"id": "leeyp1012", "name": "yeseul", "email": "leeyp1012@naver.com"}
}


# response 할 때 default 값 제외하기
@app.get("/exclude_unset/items/{item_id}", response_model=UserResponse, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


# response model include test
@app.get("/include/items/{item_id}", response_model=UserResponse, response_model_include={"city"})
async def read_item(item_id: str):
    return items[item_id]


# response model exclude test
@app.get("/exclude/items/{item_id}", response_model=UserResponse, response_model_exclude={"name"})
async def read_item(item_id: str):
    return items[item_id]


if __name__ == "__main__":
    uvicorn.run("12_response_model:app", host="localhost", port=8000, reload=True)
