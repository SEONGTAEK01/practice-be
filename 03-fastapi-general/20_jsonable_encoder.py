from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


# <jsonable encoder>
# - jsonable_encoder() -> json 화가 가능한 형태로 바꿔준다. (str 타입으로 변경)
# - model_dump() -> pydantic model 을 dict 로 바꿔준다. (기존 타입 유지)
# - model_dump_json() -> json 화가 된 형태로 바꿔준다. (key, value dict 자체가 모두 json 화 된 형태로 변경)
@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)

    model_dumped_item_data = item.model_dump()
    jsonized_item_data = item.model_dump_json()

    # json_dumped_item_data = json.dump(item)
    # json_dumpsed_item_data = json.dumps(item)

    fake_db[id] = jsonized_item_data
    return fake_db


if __name__ == "__main__":
    uvicorn.run("20_jsonable_encoder:app", host="localhost", port=8000, reload=True)
