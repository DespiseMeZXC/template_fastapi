from pydantic import BaseModel, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    url: PostgresDsn | None = None
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=".env")
    api_prefix: ApiPrefix = ApiPrefix()
    run_config: RunConfig = RunConfig()
    db_config: DatabaseConfig = DatabaseConfig()

    @property
    def database_config(self) -> DatabaseConfig:
        return DatabaseConfig(url=self.DATABASE_URL)


settings = Settings()
