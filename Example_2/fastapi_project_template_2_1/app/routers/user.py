from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.models import user as user_model
from app.deps import get_db

router = APIRouter()

@router.get("/", response_model=list[user_schema.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(user_model.User).all()