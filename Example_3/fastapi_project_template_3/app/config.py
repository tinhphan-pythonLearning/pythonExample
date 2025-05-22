from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "df2dc5311c6b46fba6d970fd7cb2e7b449f7d1242e2d62ed0f1f8e3d0d8017a9"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql+psycopg2://fastapiuser:fastapipass@db:5432/fastapidb"

    class Config:
        env_file = ".env"

settings = Settings()
