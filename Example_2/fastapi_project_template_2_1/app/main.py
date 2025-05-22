from fastapi import FastAPI
from app.routers import user
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])