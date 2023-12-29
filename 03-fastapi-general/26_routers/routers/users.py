from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["Users"])
async def read_users():
    return [{"username": "성택"}, {"username": "예슬"}]


@router.get("/users/me", tags=["Users"])
async def read_user_me():
    return {"username": "fake-current-user"}


@router.get("/users/{username}", tags=["Users"])
async def read_user(username: str):
    return {"username": username}
