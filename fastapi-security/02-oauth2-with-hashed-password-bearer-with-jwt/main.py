from datetime import timedelta, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
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
        # "disabled": True,
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
class UserInDB(User):
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
    # 아래 코드에서 shallow copy 를 한 후 to_encode.update() 를 하면 원본 'data' dict 내용도 바뀌어야 할 것 같은데 바뀌지 않음. 이유는?
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰에서 인증 정보를 찾을 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 토큰을 디코드 한 후 username 을 가져온다.
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    else:
        # 토큰에서 가져온 username 으로 DB 에서 유저 정보를 가져온다.
        user: UserInDB = get_user(fake_users_db, username)
        if not user:
            raise credential_exception
        return user

    # Exception 을 추가한다. (유저가 없는경우 / 토큰에 유저 데이터가 없는 경우)


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    # 액티브가 아니면 '비활성화 유저 입니다.' 를 리턴한다
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="비활성화 된 유저입니다.")
    return current_user


# 토큰 라우터
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # 유저 존재여부 확인 (Authentication)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="유저의 이름 또는 유저의 비밀번호가 틀렸습니다.",
                            headers={"WWW_Authenticate": "Bearer"}, )

    # 액세스 토큰 발급
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    # 토큰을 통해 유저 정보를 읽는다.
    return current_user


# <'sub' 를 쓰는 이유는?>
# - 같은 사용자에게 로그인 권한을 가진 토큰 뿐만 아니라, 다른 권한을 가진 토큰을 줄 수 있게 된다.
#   예를 들어 블로그에 글을 쓸 때 subject 를 "blog" 로 지정하여 토큰을 발급 해주면 해당 유저는 로그인 뿐만 아니라 블로그에 글을 쓸 수 있는 토큰도
#   획득하게 된다.

# <JWT 를 왜 쓸까>
# - XML 보다 단순해서 용량이 작다.
# - SWT (Simple Web Token) 은 대칭키 방식인 HMAC 을 사용하지만, JWT 는 공개키 / 개인키 방식을 사용할 수 있다.
# 이는 더 복잡한 인증방식에 사용될 수 있음을 의미한다.
# - JSON 은 대부분의 언어에서 객체로 바로 변환될 수 있다. 반면 XML 은 여러 언어에서 바로 객체로 매핑 되기가 어렵다.
# - 결론
#     - 1) 용량이 작고, 2) 프로그래밍 언어 내에서 다루기 쉽고, 3) 보안성도 높다.

# <결과를 바로 리턴하는 것과 변수를 써서 리턴하는 것의 장단점은?>
# - 바로 리턴: 코드가 짧다. 가독성이 떨어진다.
# - 변수 만들고 리턴: 코드가 1줄 추가된다. 가독성이 좋다. 디버깅 할 때 변수값을 볼 수 있다!
# - 가독성 때문에 변수를 만들고 리턴하는 것이 좋다고 생각한다.

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
