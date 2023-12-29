import uvicorn
from fastapi import FastAPI, Depends
from starlette import status

from dependencies import get_query_token, get_token_header
from internal import admin
from routers import users, items

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    dependencies=[Depends(get_token_header)],
    responses={status.HTTP_418_IM_A_TEAPOT: {"description": "I'm a teapot"}}
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
