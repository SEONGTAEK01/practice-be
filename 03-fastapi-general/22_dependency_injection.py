import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()


# <Dependency Injection>
# read_items() 와 read_users() path 가 같은 로직을 탄다고 할 때 각각의 path 에 같은 내용을 적어주는 것은 비효율 적이다.
# Depends() 를 사용해보고 DI 의 특징을 배워본다.

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# <Depends 에 클래스 사용>
# - Depends() 의 인자로 올 수 이는 것은 callable 이므로 __init__ 을 포함한 클래스 생성자도 인자로 올 수 있다는 뜻이 된다.
# - 클래스의 장점을 그대로 활용할 수 있다. (메서드, 추가변수)
# - IDE 에서 자동완성을 해주는 편리함이 있다.
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

    def get_end_index(self):
        return self.skip + self.limit


@app.get("/class_param/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    # items = fake_items_db[commons.skip:commons.skip + commons.limit]
    items = fake_items_db[commons.skip:commons.get_end_index()]
    response.update({"items": items})
    return response


# CommonQueryParams 가 타입힌트와 Depends 의 인자로 2번 반복된다. 별로이지 않은가.
# - 아래처럼 1번에 해결할 수 있다.
@app.get("/class_param_no_dup/items/")
async def read_items(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    # items = fake_items_db[commons.skip:commons.skip + commons.limit]
    items = fake_items_db[commons.skip:commons.get_end_index()]
    response.update({"items": items})
    return response


if __name__ == "__main__":
    uvicorn.run("22_dependency_injection:app", host="localhost", port=8000, reload=True)
