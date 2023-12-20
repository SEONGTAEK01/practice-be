from datetime import timedelta, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

# JWT 관련 기본 설정
SECRET_KEY = "9a70a60a1f45fb791b64b49053dd482e4fbcfd821dc7c88952ab3ecce6199b2b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 DAY

# Fake DB 데이터 생성
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# 토큰 response 스키마
class Token(BaseModel):
    access_token: str
    token_type: str


# 토큰 데이터 스키마
class TokenData(BaseModel):
    username: str | None = None


# 유저 스키마
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# 유저 DB 스키마
class UserInDB(BaseModel):
    hashed_password: str


# Password scheme 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_user(db, username) -> UserInDB:
    # 유저가 페이크 DB 에 존재하면 UserInDB 로 캐스팅 후 리턴
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)


def verify_password(plain_password, hashed_password) -> bool:
    # DB 의 hashed password 를 unhash 한 후 plain password 와 비교
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str) -> UserInDB | bool:
    # 유저 DB 존재여부 확인
    user = get_user(fake_db, username)

    # 유저가 존재하고 패스워드도 일치할 경우만 return 'True'. 그 외는 return 'False' 한다.
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # 'data' 와 'expires_delta' 를 가지고 액세스 토큰을 생성한다.
    to_encode = data.copy()  # 여기서 shallow copy 를 하는 이유는?
    to_encode.update({"exp": expire})  # .update() 의 장점은?

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # 결과를 바로 리턴하는 것과 변수를 써서 리턴하는 것의 장단점은?
    return encoded_jwt


# 토큰 라우터
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 유저 존재여부 확인 (Authentication)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="유저의 이름 또는 비밀번호가 틀렸습니다.",
                            headers={"WWW_Authenticate": "Bearer"}, )

    # 액세스 토큰 발급
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Password scheme 을 활용한 get user 만들기

# get user 와 관련된 password function 만들기

# 토큰을 활용한 'GET' Method 만들기


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
