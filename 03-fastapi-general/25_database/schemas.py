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

    # orm_mode? -2-
    # - ORM 과 orm_mode 라는 것이 잘 와닿지 않아서 조금 더 찾아봤다.
    # - Object 와 Relational-database 는 다루는 대상이 다르다. Object 는 프로그래밍 언어 내의 '객체' 가 될 것이고, Relational-database 에서는 테이블과
    # 행과 열을 가진 대상을 다룰 것이다. 따라서 프로그래밍 언어 내에서 db model 을 다루는 방법이 필요할 것이다. 그것이 ORM 이다.
    # - 어떠한 내부적 구현을 통해서 객체가 DB 모델을 가르키고 있을 것이고 DB 모델을 다루는 방법들도 ORM 에 정의가 되어있을 것이다.
    # - orm_mode=True 이면, pydantic model 의 필드가 db model (sql model) 의 'Column' 기능에 자동으로 매핑된다.
    # - ForeignKey() 기능이나 relationship() 기능도 마찬가지로 매핑될 것이다.


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
