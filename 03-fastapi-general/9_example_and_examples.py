# API 사용자가 쉽게 예제 데이터를 확인할 수 있도록 예시 데이터를 보여줄 수 있다. 방법은 여러가지가 있다.
# - class Config 사용 (Pydantic v1)
# - Field(..., example=value) 사용
# - Body 에 직접 example={} 사용
# - Body 에 직접 examples={ {"normal": {}}, {"converted":{}}, {"invalid":{}} } 사용
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


# 1. class Config 사용
# - 모델에 Config 클래스를 정의한 뒤 'schema_extra' 변수에 값을 할당하는 방법
# class Item(BaseModel):
#     name: str
#     description: str = ""
#     price: float
#     tax: float = 0.0
#
#     # Pydantic v1
#     # class Config:
#     #     json_schema_extra = {
#     #         "example": {"name": "Cafe con leche", "description": "카페 라떼", "price": 3.0}
#     #     }
#
#     # Pydantic v2
#     model_config = {
#         "json_schema_extra": {"examples": [{"name": "Cafe con leche", "description": "에스프레소 + 우유", "price": 3.0}]}}

# 2. Field(example=) 을 사용
# - 이 방법이 가독성이 좋다.
class Item(BaseModel):
    name: str = Field(..., example="Cafe con Leche")
    description: str = Field(..., example="에스프레소 + Steamed 우유")
    price: float = Field(..., example=2.4)
    tax: float = Field(0.0, example=0.05)


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# 3. Body(example=) or Body(examples=[]) 를 사용
# - 우선순위는 (라우터 인자의 Body(example=) > Field(default=) > Field(example=) 순이다.
@app.put("/items/{item_id}")
async def update_item(item_id: int,
                      item: Item = Body(...,
                                        example={"name": "Flat White", "description": "영국식 플랫 화이트"})):
    results = {"item_id": item_id, "item": item}
    return results


# 4. Body(openapi_examples=)
# - 추가적인 메타정보를 담을 수 있다. ('summary', 'description', 'value', 'externalValue')
@app.put("/items/{item_id}")
async def update_item(*,
                      item_id: int,
                      item: Annotated[
                          Item,
                          Body(
                              openapi_examples={
                                  "normal": {
                                      "summary": "기본 메뉴 아이템 설명",
                                      "description": "1년 내내 항상 제공하는 메뉴",
                                      "value": {
                                          "name": "Espresso",
                                          "description": "1 샷 에스프레소"
                                      }
                                  },
                                  "seasonal": {
                                      "summary": "시즈널 메뉴 아이템 설명",
                                      "description": "여름 / 겨울 에만 제공하는 메뉴",
                                      "value": {
                                          "name": "Cafe bonbon",
                                          "description": "에스프레소 더블 + 연유"
                                      }
                                  }
                              }
                          )
                      ],
                      ):
    results = {"item_id": item_id, "item": item}
    return results


if __name__ == "__main__":
    uvicorn.run("9_example_and_examples:app", host="localhost", port=8000, reload=True)
