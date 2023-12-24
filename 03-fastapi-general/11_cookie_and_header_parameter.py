import uvicorn
from fastapi import FastAPI, Cookie, Header

app = FastAPI()


# <Cookie Class>
# - Request header 에 쿠키가 있다면 쿠키 내용을 읽는다.
# - e.g.) curl -X 'GET' 'http://localhost:8000/cookie-test/items/' -H 'accept: application/json' -H 'Cookie: name=TAEK'
# {"name":"TAEK"}
# - 쿠키에 'name' 이라는 키, 밸류가 있으면 자동으로
@app.get("/cookie-test/items/")
async def read_items(name: str | None = Cookie(None)):
    return {"name": name}


# <Header Class>
# - Request header 의 키 값을 헤더형태로 적절히 변환해준다.
# - 예를 들어 유저가 'user-agent' 라는 키값을 포함해 요청을 했다고 하자. Header 클래스를 할당하여 변수를 만들면,
#    'user-agent' 키 값을 보내도 'user_agent' 로 자동으로 변환해준다. 파이썬에서는 dash (-) 가 포함된 변수명을 만들 수 없기 때문이다.
@app.get("/header-test/items/")
async def read_items(user_agent: str | None = Header(None)):
    return {"User-Agent": user_agent}


# <중복 Header 다루기>
# - 같은 Header 가 여러번 오는 경우 를 리스트로 처리할 수 있다.
@app.get("/duplicate_headers/items/")
async def read_items(x_token: list[str] = Header(None)):
    return {"Token Values": x_token}


if __name__ == "__main__":
    uvicorn.run("11_cookie_and_header_parameter:app", host="localhost", port=8000, reload=True)
