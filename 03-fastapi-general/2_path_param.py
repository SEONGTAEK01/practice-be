import uvicorn
from fastapi import FastAPI

app = FastAPI()


# Path operation 은 순서가 있다.
# /users/me 가 호출될 경우 등록된 순서대로 호출된다.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("2_path_param:app", host="localhost", port=8000, reload=True)
