from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración del backend.

    Los campos sin valor por defecto son obligatorios: el arranque falla si faltan.
    Los valores confirmados en el README se cargan desde el entorno, no se codifican aquí.
    """

    model_config = SettingsConfigDict(
        # El .env de la raíz del repo (al ejecutar desde backend/) y uno local opcional.
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
