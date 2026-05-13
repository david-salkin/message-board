from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

cwd = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(cwd, "..", "..", ".env")  # core -> app -> root

# environment variables will ioverride these hard settings
class Settings(BaseSettings):

	SECRET_KEY: str = ""  # keep pylance happy but check it below
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
	ALGORITHM: str = "HS256"
	app_name: str = "message-board"
	debug: bool = False
	sql_debug: bool = False

	model_config = SettingsConfigDict(env_file=env_path)

cfg_settings = Settings()

# CRITICAL
if not cfg_settings.SECRET_KEY:
	raise ValueError(
		f"SECRET_KEY is empty! Check if {env_path} exists and contains 'SECRET_KEY=your_secret'")
