from enum import StrEnum

import uvicorn
from fastapi import FastAPI

app = FastAPI()


# 리퀘스트 값을 제한하고 싶다. -> StrEnum 을 사용한다.
# value 값이 string 인 것이 StrEnum 이다.
class MenuDetail(StrEnum):
    espresso = "espresso"
    americano = "americano"
    caffe_latte = "caffe_latte"


@app.get("/menu/{cafe_menu}")
async def get_cafe_menu_detail(cafe_menu: MenuDetail):
    if cafe_menu == MenuDetail.espresso:
        return {"cafe_menu": cafe_menu, "detail": "Espresso double shots with sugar"}

    if cafe_menu.value == "caffe_latte":
        return {"cafe_menu": cafe_menu, "detail": "Espresso + water + milk"}

    if cafe_menu.value == "americano":
        return {"cafe_menu": cafe_menu, "detail": "Espresso with 300 mL water"}


if __name__ == "__main__":
    uvicorn.run("1_string_enum:app", host="localhost", port=8000, reload=True)
