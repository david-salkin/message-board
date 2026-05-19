from pydantic_settings import BaseSettings, SettingsConfigDict
import os

model_config_dict = SettingsConfigDict(
    env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
    env_file_encoding="utf-8",
    extra="ignore" # allows .env file to have extra variables without causing Pydantic crash
)

# environment will override these settings
class Settings(BaseSettings):

	model_config = model_config_dict

	SECRET_KEY: str = ""  # keep pylance happy but check it below
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
	ALGORITHM: str = "HS256"
	app_name: str = "message-board"
	debug: bool = False
	sql_debug: bool = False
	DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"


cfg_settings = Settings()

# Critical that SECRET_KEY is set in env
if not cfg_settings.SECRET_KEY:
	raise ValueError("SECRET_KEY is empty! Check your root .env file mapping initialization contexts.")
