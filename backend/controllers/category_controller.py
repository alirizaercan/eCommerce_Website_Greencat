# controllers/category_controller.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.category import Category
from database import get_db

router = APIRouter()

@router.get("/categories/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/categories/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
