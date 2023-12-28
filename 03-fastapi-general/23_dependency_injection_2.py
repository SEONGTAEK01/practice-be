import uvicorn
from fastapi import FastAPI, Depends, Cookie, Header, HTTPException
from starlette import status

app = FastAPI()


# <Sub Dependency>
# - 원하는 만큼 여러개의 sub dependency 를 생성할 수 있다.
# - 여기서는 query 또는 cookie extractor dependency 를 만들어 보자.
# - query param 이 존재하면 q 를 리턴하고, 그렇지 않으면 Cookie() 를 리턴한다.

def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: str = Cookie(None)):
    if q:
        return q
    return last_query


@app.get("/items/")
async def read_items(query_or_cookie=Depends(query_or_cookie_extractor)):
    return {"query_or_cookie": query_or_cookie}


# <Path Operation DI>
# - 만약 리턴값이 필요하지 않고 반드시 실행은 해야 한다면 Path operation decorator 에 dependency 를 걸어주면 된다.
# - 사용방법은 데코레이터에 'dependencies=[Depends(), Depends()]' 형태로 넣어주면 된다.
def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid!")


def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Key header invalid!")
    return x_key  # x_key 를 리턴하지만 path operation 에 전달되지 않는다.


@app.get("/path_operator_di/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "foo"}, {"item": "bar"}]


# <어플리케이션 전체에 depends 걸기>
# - 앱 전체에 디펜던시를 걸 수도 있다.
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# <cleanup 코드로 'yield' 사용하기>
# - FastAPI 에서 dependency 가 끝나면 yield 를 사용하여 cleanup 작업을 할 수 있다.
# - 대표적으로 데이터베이스 close() 작업이 있다.
# - 'yield' 대신 'return' 을 하면 에러가 발생하든 안하든 .close() 는 실행되지 않는다.
# async def get_db():
#     db = DBSession()
#     try:
#         yield db
#     finally:
#         db.close()

if __name__ == "__main__":
    uvicorn.run("23_dependency_injection_2:app", host="localhost", port=8000, reload=True)
