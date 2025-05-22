from fastapi import FastAPI
from app.routers import user, auth
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI JWT Auth with Alembic and PostgreSQL")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
