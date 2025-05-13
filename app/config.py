from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[str]
    # BASE_URL: str
    use_webhook: bool = False
    DB_URL: str | None = f"postgresql+asyncpg://test"
    # @property
    # def hook_url(self) -> str:
    #    """Возвращает URL вебхука"""
    #    return f"{self.BASE_URL}/webhook"

    # @property
    # def url(self) -> str:
    #    return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.NAME}"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
