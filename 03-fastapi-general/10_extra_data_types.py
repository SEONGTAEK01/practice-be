# <Extra Data Types>
# - API request 또는 response 받을 때의 데이터 타입과, 요청받은 내용을 FastAPI 내에서 처리할 때 타입이 항상 같지는 않다.
# - 예를 들어 datetime.date, datetime.datetime 등은 request, response 시 'str' 으로 처리된다.
# - 하지만 FastAPI 내부에서는 본래 파이썬 그대로의 타입인 datetime.date 또는 datetime.datetime 으로 처리된다.


# 따라서 request 와 response 시에 타입이 어떻게 변환되는지를 아는 것은 중요하다.
# 경우에 따라서, request, response 시에 서로 다른 타입이 FastAPI 내에서는 같은 타입으로 취급되어 연산이 가능하기도 하다.
# - datetime.timedelta (str in request, response)
# - datetime.date (str in request, response)
# - 위처럼 request, response 에서는 모두 str 타입이지만, FastAPI 에서는 같은 datetime 타입으로 취급된다.
# - 따라서 API 내에서 datetime.timedelta 와 datetime.date 의 연산이 가능해진다.

from datetime import datetime, time, timedelta

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    start_datetime: datetime | None
    end_datetime: datetime | None
    repeat_at: time | None
    process_after: timedelta | None


class ItemResponse(Item):
    item_id: int
    start_after: datetime | None
    duration: timedelta | None


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
        item_id: int,
        item: Item
):
    # 방법 1
    # item.start_after = item.start_datetime + item.process_after
    # item.duration = item.end_datetime - item.start_datetime
    # return {"item_id": item_id, "start_after": start_after, "duration": duration, **item.model_dump()}

    # 방법 2
    # - ItemResponse 를 정의해서 return 해본다.
    response = ItemResponse(**item.model_dump(),
                            item_id=item_id,
                            start_after=item.start_datetime + item.process_after,
                            duration=item.end_datetime - item.start_datetime)
    return {**response.model_dump()}


if __name__ == "__main__":
    uvicorn.run("10_extra_data_types:app", host="localhost", port=8000, reload=True)
