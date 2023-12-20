from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# TODO:
# 1. User DB 생성 부분
# 2. 로그인 요청 시 패스워드 비교하는 부분

# User schema
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# User DB 생성 부분
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


# 가짜 hasehd password 생성
def fake_hashed_password(password: str) -> str:
    return "fakehashed" + password


# Callable 인 oauth2_scheme 을 넣어주면 Authorization 헤더에서 bearer token 분리 후
# token 을 리턴 한다. callable 인지는 __call__ 이 있으면 알 수 있다.
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Check user
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username")

    # Check password
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Return token
    return {"access_token": user.username,
            "token_type": "bearer"}


def get_user(db, username: str):
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    # User 를 fake db 에서 가져온다. token 은 username 을 담고있다.
    user = get_user(fake_users_db, token)
    return user


# oauth2_scheme 의 결과로 token 을 받아온다. oauth2_scheme 은 유저 요청을 parsing 해서 토큰을 가져온다.
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # token 을 fake db 에 넣어서 유저 정보를 가져온다.
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
