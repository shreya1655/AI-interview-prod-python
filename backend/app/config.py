from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    database_url: str = "sqlite:///./interviews.db"
    daily_global_limit: int = 50
    daily_user_limit: int = 5
    allowed_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
