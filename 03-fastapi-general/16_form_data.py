import uvicorn
from fastapi import FastAPI, Form

app = FastAPI()


# <Form Data 로 request 를 받을 때 처리>
# - HTML forms (<form></form>) 데이터는 특별한 인코딩 방식을 통해 서버로 전송된다.
# - 따라서 JSON 형태의 request 와는 다르게 Form data 를 처리하는 방식이 필요하다.
# - Form() 을 사용하면 된다.
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"user_name": username, "password": password}


# <request 방식에 따른 헤더와 데이터의 차이>
# query string 의 경우
# e.g.) curl -X 'POST' \
#   'http://localhost:8000/items/?name=taek' \
#   -H 'accept: application/json' \
#   -d ''

# request body 의 경우
# curl -X 'POST' \
#   'http://localhost:8000/user/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "username": "string",
#   "email": "user@example.com",
#   "full_name": "string",
#   "password": "string"
# }'

# form data 의 경우
# curl -X 'POST' \
#   'http://localhost:8000/login/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/x-www-form-urlencoded' \
#   -d 'username=sabitz&password=1234'


if __name__ == "__main__":
    uvicorn.run("16_form_data:app", host="localhost", port=8000, reload=True)
