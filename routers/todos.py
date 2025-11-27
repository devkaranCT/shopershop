from fastapi import APIRouter, Depends, HTTPException, Path
from models import Items
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0 , lt=6)
    complete: bool

@router.get("/all-products", status_code=status.HTTP_200_OK)
def read_all_products(db: db_dependency):
    return db.query(Items).all()

@router.get("/search-product/{search_string}", status_code=status.HTTP_200_OK)
def search_products(db: db_dependency, search_string: str):
    todo_model = db.query(Items).filter(Items.title.ilike(f"%{search_string}%")).all()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.get("/product/{product_id}", status_code=status.HTTP_200_OK)
def get_product_detail(db: db_dependency, product_id: int = Path(gt=0)):
    todo_model = db.query(Items).filter(Items.id == product_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.post("/add-product", status_code=status.HTTP_201_CREATED )
def add_product(db: db_dependency, todo_request: TodoRequest):
    todo_model = Items(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@router.put("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_product(db: db_dependency, todo_request: TodoRequest, product_id: int = Path(gt=0)):
    todo_model = db.query(Items).filter(Items.id == product_id).first()
    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(db: db_dependency, product_id: int = Path(gt=0)):
    todo_model = db.query(Items).filter(Items.id == product_id).first()
    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Not found")