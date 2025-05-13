from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    use_webhook: bool = False

    # @property
    # def hook_url(self) -> str:
    #    """Возвращает URL вебхука"""
    #    return f"{self.BASE_URL}/webhook"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class OgasStuffDBSettings(BaseSettings):
    name: str
    user: str
    password: SecretStr
    host: str
    port: int = 5432

    class Config:
        env_prefix = "OGAS_STUFF_DB_"
        env_file = ".env"
        extra = "ignore"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


settings = Settings()
ogas_stuff_db_settings = OgasStuffDBSettings()
