import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
)


Base = declarative_base()


def get_session():
    session = SessionLocal()

    try:
        yield session
    except:
        session.close()
