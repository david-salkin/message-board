from pydantic import BaseSettings

# environment variables will ioverride these hard settings
class Settings(BaseSettings):

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    app_name: str = "message-board"
    debug: bool = False

    class Config:
        env_file = ".env"


cfg_settings = Settings()