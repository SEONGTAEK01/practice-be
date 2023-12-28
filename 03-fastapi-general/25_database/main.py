import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from crud import get_user_by_email, get_users, get_user, create_item, get_items
from crud import create_user as crud_create_user
from database import engine, Base, SessionLocal
from schemas import UserCreate, ItemCreate, User, Item

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 유저가 존재하면 raise exception
    # 아니면 생성
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    created_user = crud_create_user(db, user)
    return created_user


@app.get("/users/", response_model=list[User], status_code=status.HTTP_200_OK, tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = get_users(db, skip, limit)
    return db_users


@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK,tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    # 항상 exception handling 을 생각해서 코드 작성 해야함
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model=Item, tags=["Items"])
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    created_item = create_item(db, item, user_id)
    return created_item

@app.get("/items/", response_model=list[Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_items = get_items(db,skip,limit)
    return db_items


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
