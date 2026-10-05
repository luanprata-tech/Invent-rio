from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventário & IPAM API"
    SECRET_KEY: str = "verysecretkey" # TODO: Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"

settings = Settings()
