from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_hostname: Optional[str] = None
    database_port: Optional[str] = None
    database_password: Optional[str] = None
    database_name: Optional[str] = None
    database_username: Optional[str] = None
    secret_key: Optional[str] = None
    algorithm: Optional[str] = None
    access_token_expire_minutes: Optional[int] = None

    model_config = SettingsConfigDict(env_file=".env")

settings: Settings = Settings()