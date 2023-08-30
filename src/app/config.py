from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import loguru

log = loguru.logger

load_dotenv()


class Setting(BaseSettings):
    # region Database
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return (
            f'postgresql+psycopg2://{values["POSTGRES_USER"]}:{values["POSTGRES_PASSWORD"]}@'
            f'{values["POSTGRES_HOST"]}:{values["POSTGRES_PORT"]}/{values["POSTGRES_DB"]}'
        )

    # endregion

    # region Telegram
    TG_TOKEN: str
    TG_ADMIN_ID: int
    # endregion

    # region Templates
    TEMPLATES_DIR: str = "app/jinja_templates"
    # endregion

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"
        env_file = ".env"


settings = Setting()  # type: ignore
