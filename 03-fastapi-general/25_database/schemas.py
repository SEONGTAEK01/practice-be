from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
    # orm_mode?
    # - Item 은 pydantic model 이지 dict 가 아니지만, dict 처럼 값을 읽고 쓸 수 있게 해준다.
    # - orm_mode=True 로 해야 relation 걸린 데이터를 같이 끌고온다.
    #    - e.g.) current_user.items 처럼 접근해야 relation 걸린 데이터를 가져오는데, orm_mode=True 로 하면 sql alchemy model 이 pydantic
    #    model 로 변환될 때 자동으로 relation 걸린 데이터를 끌고온다.
    # - 위처럼 current_user.items 를 통해 명시적으로 접근하기 전까지 데이터가 로딩되지 않는 것을 lazy-loading 이라고 한다.


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
