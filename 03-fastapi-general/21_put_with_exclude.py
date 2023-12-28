# <put w/ 'exclude_unset'>
# - put 은 model 전체를 업데이트 하는 것인데 요청에 일부 필드가 없다면 어떻게 업데이트가 될까?
# - model 에 디폴트 값이 있다면 그 값으로 업데이트가 된다.
# - 따라서 missing 필드가 없도록 하거나, model_dump() 시에 해당 필드를 'exclude_unset' 시켜야 한다.
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

app = FastAPI()


# put w/o 'tax' field
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    # 일단 exclude_unset=False 로 업데이트 해보자.
    # - 결과: 'tax' 필드에 model default 값인 10.5 가 의도치 않게 들어가 버린다. exclude_unset 지정하자.
    # input = item.model_dump(exclude_unset=True)
    # items[id] = Item(**input)

    # 업데이트 요청된 데이터만 데이터베이스에 저장하자
    # - 기존 데이터를 DB 에서 가져온다.
    # - 가져온 데이터를 모델화 한다.
    # - 요청한 데이터를 dict 화 한다. (exclude_unset=True 활용)
    # - DB 에서 가져온 데이터를 요청 받은 데이터로 덮어쓴다.
    # - DB 에 저장가능한 형태로 convert 하기 위해 jsonable_encoder() 사용한 후 DB 에 저장한다.
    # - updated item model 을 리턴한다.
    stored_item = items[item_id]
    stored_item_model = Item(**stored_item)

    update_data: dict[str, Any] = item.model_dump(exclude_unset=True)
    updated_item: Item = stored_item_model.model_copy(update=update_data)

    items[item_id] = jsonable_encoder(updated_item)
    return items


if __name__ == "__main__":
    uvicorn.run("21_put_with_exclude:app", host="localhost", port=8000, reload=True)
