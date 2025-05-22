from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, core
from app.deps import get_db, get_current_user


router = APIRouter()

@router.post("/", response_model=schemas.user.UserResponse)
def create_user(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = core.security.get_password_hash(user_in.password)
    new_user = models.user.User(email=user_in.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=schemas.user.UserResponse)
def read_current_user(current_user: models.user.User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=schemas.user.UserResponse)
def update_user(user_id: int, user_in: schemas.user.UserUpdate, db: Session = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user.email = user_in.email
    user.hashed_password = core.security.get_password_hash(user_in.password)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(user)
    db.commit()
    return
