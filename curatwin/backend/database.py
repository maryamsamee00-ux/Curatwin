from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from .config import AUTO_CREATE_TABLES, DATABASE_URL, IS_SQLITE

if IS_SQLITE:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        # Serverless functions are frozen between invocations, so a client-side
        # pool just holds Postgres connections hostage. Neon's pooled endpoint
        # does the real pooling. NullPool = one connection per request, closed
        # on release.
        poolclass=NullPool,
        connect_args={
            "sslmode": "require",
            "connect_timeout": 10,
            # Pin the session TZ so server_default=func.now() lands as UTC and
            # matches the naive datetime.utcnow() windows in the routers.
            "options": "-c timezone=UTC",
        },
        future=True,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

_tables_ready = False


def _ensure_tables():
    global _tables_ready
    if _tables_ready or not AUTO_CREATE_TABLES:
        return
    init_db()
    _tables_ready = True


def get_db():
    _ensure_tables()
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Create missing tables. Idempotent. On Postgres run once via scripts/init_db.py."""
    from . import models  # noqa: F401 registers all mappers on Base
    Base.metadata.create_all(bind=engine)
