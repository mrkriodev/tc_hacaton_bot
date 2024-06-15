from aiogram.types import BotCommand
from pydantic import (
    PostgresDsn,
)

from pydantic_settings import BaseSettings

bot_command = [
    BotCommand(command="start", description="Запуск бота"),
    BotCommand(command="help", description="Помощь и описание функционала"),
    BotCommand(command="menu", description="Получение главного меню"),
]


class WebHookSettings(BaseSettings):
    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080

    WEBHOOK_PATH: str = "/webhook"
    WEBHOOK_SECRET: str = "my-secret"
    BASE_WEBHOOK_URL: str = "https://aiogram.dev/"


class Settings(BaseSettings):
    DEBUG_MODE_POSTGRES: bool
    BOT_TOKEN: str
    POSTGRES_DSN: PostgresDsn
    START_POOLING: bool
    WEBHOOK_SETTINGS: WebHookSettings | None = None
    ANALYZE_SERVICE_URL: str
    ANALYZE_SERVICE_BASE_URL: str
    ANALYZE_SOCIAL_INFO_URL: str
    ANALYZE_AI_URL: str
    ANALYZE_SERVICE_SOURCE_CODE_URL: str
    ANALYZE_SERVICE_LIQUIDITY_URL: str
    ANALYZE_SERVICE_TRANSFER_URL: str


settings = Settings(_env_file=".env", _env_file_encoding="UTF-8")
