import uvicorn
from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

app = FastAPI()

items = {"foo": "The Foo Fighters"}


# <Handling Errors>
# - HTTPException 은 Exception 에 HTTP 관련 에러를 추가한 것이다.
# - 따라서 return 이 아닌 raise 해주어야 한다.
# - 그냥 return 하면 클래스 정보가 리턴된다. 에러 raise 도 안된다. 200 OK 가 뜬다! 리턴에 성공했으니까.

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found",
                            headers={
                                "X-Error": "There goes my error!"})
        # Response header 에 커스텀 헤더를 넣을 수도 있다. 보안상의 이유로 필요할 때가 있다고 함.
    return {"item": items[item_id]}


# <Custom Exception & Handler>
# - Exception 을 상속하는 Custom exception 을 만들 수 있다. 방법은 아래와 같다.
# - 1. Custom Exception Class 를 만든다.  2. Exception Handler 를 등록한다.

# <Custom Exception & Handler 만들어 보기>
# - '메리아종' 이라는 이름의 말이 들어오면 UnicornException 을 발생 시킨다.
# - Output: Exception handler 에서 '메리아종' 이라는 이름을 출력한다.

# Exception 클래스 생성
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


# Exception 클래스 등록
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(status_code=status.HTTP_418_IM_A_TEAPOT,
                        content={"message": f"Oops! {exc.name} did something!"})


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "메리아종":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# <기존 Exception Override>
# - Custom Exception 을 만들수도 있지만 기존 Exception 을 override 할 수도 있다.
# - FastAPI 의 RequestValidationError 를 override 해보자.
# - 422 Unprocessable Entity 에러가 override 를 통해 400 Bad Request 를 plain text 로 내려주도록 바뀌었다.
@app.exception_handler(RequestValidationError)
async def custom_request_validation_error_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc.errors()), status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/custom-exception-handler/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "무야무야":
        raise RequestValidationError(errors={"msg": f"I don't like {name}"})
    return {"unicorn_name": name}

# FastAPI 의 기본 exception handler 를 사용할 수도 있다.
@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await http_exception_handler(request, exc)


if __name__ == "__main__":
    uvicorn.run("18_handling_errors:app", host="localhost", port=8000, reload=True)
