# query param 을 Query() 로, path param 을 Path() 로, request body 를 Body() 로 세세하게 다루듯,
# request body 안의 fields 를 Field() class 로 세세하게 다룰 수 있다.
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    # url: str

    # 일반 str type 이 아닌 pydantic type 을 지정해 줄 수 있다. Annotated[Url, UrlConstraints] 로 구성되어 있음. 'http' or
    # 'https' url 만 request body 에 실을 수 있다.
    url: HttpUrl

    description: str = ""


class Item(BaseModel):
    name: str
    price: float = Field(None, title="메뉴 가격", ge=0)
    description: str | None = Field(..., title="메뉴 설명")

    tags: list[str | int] = Field([], title="중복 허용 태그")  # tags 가 가질 타입 (list) 와 list 의 타입 (str or int) 를 명시적으로 지정할 수 있다.
    no_duplication_tags: set[str] = Field(set(), description="중복 tag 가 들어오면 제거하도록 설계된 tag")

    # image: Image | None = None  # 모델은 다른 모델 안에 nested 될 수 있다.
    images: list[Image] = Field([], description="복수 image 를 담는 리스트형 필드")


# Item 을 put 하는 메서드를 만들고 Item model 에 Field() 를 추가해본다.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# 중첩 nested 도 가능하다.
class Offer(BaseModel):
    description: str | None = Field(None, description="오퍼 설명")
    name: str
    price: float
    items: list[Item] = Field(..., description="오퍼를 구성할 아이템")


# 중첩 nested 예시
@app.post("/offers")
async def create_offer(offer: Offer):
    return offer


# 바디로 json list 받기
@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


# 범용 목적의 request body 에 dict 를 사용한 예
@app.post("/menu")
async def create_menu(menu: dict[str, str]):
    return menu


if __name__ == "__main__":
    uvicorn.run("8_field_class:app", host="localhost", port=8000, reload=True)
