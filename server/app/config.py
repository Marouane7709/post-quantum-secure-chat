import base64
import json
import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from pydantic import Field
from pydantic_settings import BaseSettings

SECRETS_PATH = Path(__file__).resolve().parent.parent / "secrets.json"


def _load_or_create_secrets() -> Dict[str, str]:
    data: Dict[str, str]
    if SECRETS_PATH.exists():
        data = json.loads(SECRETS_PATH.read_text())
    else:
        data = {}
    changed = False
    if "secret_key" not in data:
        data["secret_key"] = secrets.token_urlsafe(48)
        changed = True
    if "crypto_master_key" not in data:
        data["crypto_master_key"] = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        changed = True
    if changed:
        SECRETS_PATH.write_text(json.dumps(data, indent=2))
    return data


_persisted = _load_or_create_secrets()


class Settings(BaseSettings):
    app_name: str = "PQ Secure Messenger"
    database_url: str = "sqlite:///./pqchat.db"
    secret_key: str = Field(default_factory=lambda: _persisted["secret_key"])
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    crypto_master_key: str = Field(default_factory=lambda: _persisted["crypto_master_key"])

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


