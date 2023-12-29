from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "성택"}, {"username": "예슬"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fake-current-user"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
