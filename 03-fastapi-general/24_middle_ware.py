import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# <Middleware>
# - 미들웨어란 path operation 이 실행되기 전/후에 중간에 어떤 프로세스를 실행시키는 중간자를 말한다.
# - Client <-> Middleware <-> Path operation
# - Client 와 Path operation 사이에 항상 무언가를 처리해주고 싶을 때 사용한다.
# - 'call_next' 는 다음에 실행될 path operation 이다.
# - custom proprietary header 를 사용하려면 관습적으로 'X-' 를 붙인다. (붙였다?)
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


# <CORS Middleware>
# - CORS 는 Cross Origin Resource Sharing 이다. 서로 다른 리소스 간의 공유여부를 설정하는 부분이다.
# - Origin 이란 뭘까? protocol (http/https) + domain (myapp.com/localhost) + port(80/8080) 3가지의 조합을 의미한다.
# - 따라서 3개 중 1개라도 다르면 다른 출처이다.
# - e.g.) http://localhost, https:/localhost, http://localhost:8080 은 모두 다른 출처이다.

# <설명 참조>
# - https://evan-moon.github.io/2020/05/21/about-cors/#preflight-request
# - https://velog.io/@awesome-hong/HTTP-Options-%EC%9A%94%EC%B2%AD%EC%9D%80-%EB%AD%98%EA%B9%8C

# <실습>
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,  # Authorization header, Cookie 를 말한다.
    allow_methods=["*"],  # PUT, POST 등
    allow_headers=["*"]
)


@app.get("/")
async def main():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    uvicorn.run("24_middle_ware:app", host="localhost", port=8000, reload=True)
