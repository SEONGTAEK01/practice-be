# <Multiple Response Model 의 활용 사례 2>

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Model 정의
class ItemBase(BaseModel):
    description: str
    type: str


class CarItem(ItemBase):
    type: str = "car"


class PlaneItem(ItemBase):
    type: str = "plane"
    size: int


# Item 정의
items = {
    "1": {"description": "Low rider...!", "type": "car", },
    "2": {"description": "Maverick", "type": "plane", "size": 5, }
}


# Router 정의
# - FastAPI 공식문서에는 response_model 에 Union 을 넘겨주어야 하고 type annotation 방식으로 넘겨주면 오류가 발생한다고 되어 있는데
#   오류가 나지 않는다. (https://fastapi.tiangolo.com/ko/tutorial/extra-models/#__tabbed_3_1)
# - PEP 604 (https://peps.python.org/pep-0604/) 부터 허용된 듯?
# @app.get("/items/{item_id}", response_model=Union[PlaneItem | CarItem])
@app.get("/items/{item_id}", response_model=PlaneItem | CarItem)
async def read_items(item_id: str):
    return items[item_id]


# <Response Model 에 list 타입 사용하기>
items_list = [{"description": "Low Rider 1"}, {"description": "Low Rider 2"}]


@app.get("/list/items", response_model=list[CarItem])
async def read_items_list():
    return items_list


# <일반 object return 예시>
@app.get("/dict-type/items", response_model=dict[str, float])
async def read_items():
    return {"Low Rider 1": 384.2, "Low Rider 2": 548.2}


if __name__ == "__main__":
    uvicorn.run("14_extra_model_2:app", host="localhost", port=8000, reload=True)
