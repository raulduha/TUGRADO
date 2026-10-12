from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import get_settings


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def get_db(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    # Los servicios confirman sus transacciones; al cerrar se descarta lo no confirmado.
    with Session(engine) as db:
        yield db
