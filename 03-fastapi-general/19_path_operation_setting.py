# <Path operation setting>
# - Path operation (/blah/item) 과 관련된 설정 하는 법을 배워보자.
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


# <status_code, tags, summary, and description 추가 가능>
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"],
          summary="Create an item",
          description="Create an item with all the information, name, description, price, tax, and set of tags")
async def create_item(item: Item):
    return item


# <description 표기의 다른 방법>
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"],
          summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


if __name__ == "__main__":
    uvicorn.run("19_path_operation_setting:app", host="localhost", port=8000, reload=True)
