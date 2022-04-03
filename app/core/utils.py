from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os



def get_mysql_uri() -> str:
    user = os.environ.get("DB_USER", "root")
    host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "softly")
    password = os.environ.get("DB_PASSWORD", "zeca1234")
    port = 3306 if host == "localhost" else 33060
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"


# TODO criar scripts .sh para testes e criar script python para migrations sem problemas de path
# set PYTHONPATH=. or export PYTHONPATH=.
# alembic revision --autogenerate -m "Added initial tables"
# alembic upgrade head

# TODO criar script para popular banco e limpar tabelas.


def get_server_uri() -> str:
    pass


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        get_mysql_uri(),
        isolation_level="SERIALIZABLE",
    ),
    autocommit=False,
    autoflush=False,
)


def get_db_session() -> Generator:
    try:
        db = DEFAULT_SESSION_FACTORY()
        yield db
    finally:
        db.close()

def get_session() -> Session:
    try:
        db = DEFAULT_SESSION_FACTORY()
        return db
    finally:
        db.close()
