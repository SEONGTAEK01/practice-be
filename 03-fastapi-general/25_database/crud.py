from sqlalchemy.orm import Session

from models import User, Item
from schemas import UserCreate, ItemCreate


# Read User
# - SQLAlchemy model 을 사용한다. "DB 에서 부터" 데이터를 읽는 과정이기 때문이다.
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


# Create User
# - Pydantic model 을 사용한다. "API 요청으로 부터" 온 데이터 이기 때문이다.
def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "not-really-hashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Read Item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


# Create Item
def create_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
