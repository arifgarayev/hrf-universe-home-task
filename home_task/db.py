import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

import config  # for alembic migration to detect env vars

engine = create_engine(
    f'{os.getenv("POSTGRES_DRIVER")}://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")@{os.getenv("POSTGRES_HOST")} if not os.getenv("IS_LOCAL") else "localhost"}/{os.getenv("POSTGRES_DB")}',
)
pg_session_factory = sessionmaker(
    engine, Session, autocommit=False, autoflush=False, expire_on_commit=False
)
SessionFactory = scoped_session(pg_session_factory)


def get_session() -> Session:
    return SessionFactory()
