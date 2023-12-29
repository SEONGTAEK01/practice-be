from fastapi import HTTPException, Depends, APIRouter, Header
from starlette import status


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


router = APIRouter(
    prefix="/items", tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"수저": {"name": "김씨 방짜 수저"}, "젓가락": {"name": "방짜 젓가락"}}


@router.get("/", status_code=status.HTTP_200_OK)
async def read_items():
    return fake_items_db


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item_id": item_id, "name": fake_items_db.get(item_id).get("name")}


@router.put("/{item_id}", status_code=status.HTTP_200_OK, tags=["custom"])
async def update_item(item_id: str):
    # 없으면 에러
    # 있으면 'name' 변경
    if item_id not in fake_items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    fake_items_db[item_id]["name"] = "Name modified"
    return fake_items_db[item_id]
