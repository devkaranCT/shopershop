from fastapi import APIRouter, Depends, HTTPException, Path
from models import Items
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user


router = APIRouter(
    tags=["cart"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0 , lt=6)
    complete: bool

@router.get("/all-products-in-cart", status_code=status.HTTP_200_OK)
def read_all_products_added_to_cart(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    return db.query(Items).filter(Items.owner_id == user.get("user_id")).all()


@router.post("/add-product-to-cart", status_code=status.HTTP_201_CREATED )
def add_product_to_cart(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")
    print(user)
    print(user.get("username"))
    print(user.get("user_id"))
    todo_model = Items(**todo_request.model_dump(), owner_id= user.get("user_id"))
    db.add(todo_model)
    db.commit()


@router.delete("/delete-product-from-cart/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_from_cart(user: user_dependency, db: db_dependency, product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")

    todo_model = db.query(Items).filter(Items.id == product_id).first()
    if todo_model is not None:
        todo_model.owner_id = None
        db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Not found")