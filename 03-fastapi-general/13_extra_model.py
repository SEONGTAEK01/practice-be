import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# <Multiple Response Model 의 활용 사례 1>
# - Pydantic model 로 모델링 할 때 아래와 같은 상황이 종종 발생한다.
# - input model: 유저 password 필드가 필요하다.
# - response model: 유저 password 필드가 필요없다.
# - database model: hashed password 가 필요하다.
# - 따라서 아래와 같이 각각의 모델을 만들어서 해결할 수 있다.
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: Optional[str] = None


# 하지만 각 모델의 필드가 중복되는 부분이 많다. 이를 어떻게 해결할까?
# - 공통 부분을 UserBase 모델로 만들어서 분리하고 상속하는 것이다.
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None | None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


if __name__ == "__main__":
    uvicorn.run("13_extra_model:app", host="localhost", port=8000, reload=True)
