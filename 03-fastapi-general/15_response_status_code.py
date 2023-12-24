import uvicorn
from fastapi import FastAPI
from starlette import status

app = FastAPI()


# status_code 를 넣지 않으면 요청이 성공할 경우 그냥 200 OK 를 내려준다.
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


# HTTP Status Code 의미
# - 1xx: Information 을 뜻함. 거의 사용할 일 없음
# - 2xx: OK (201: Created, 204: No Content)
# - 3xx: Redirection
# - 4xx: Client-side error (대부분 요청 오류)
# - 5xx: Server-side error (실제로 명시할 일 거의 없음. 서버 오류일 경우 알아서 5xx 를 보게된다.)

if __name__ == "__main__":
    uvicorn.run("15_response_status_code:app", host="localhost", port=8000, reload=True)
