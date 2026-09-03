import os
import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IS_VERCEL = bool(os.environ.get("VERCEL"))

# ---------------------------------------------------------------- secrets ----
SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()
if not SECRET_KEY:
    if IS_VERCEL:
        raise RuntimeError(
            "SECRET_KEY is required in production. Set it in the Vercel "
            "dashboard under Settings -> Environment Variables."
        )
    SECRET_KEY = "dev-only-insecure-key-never-use-in-production"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


# --------------------------------------------------------------- database ----
def _normalize(url: str) -> str:
    """Vercel/Neon hand out 'postgres://'; pin the driver explicitly."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix):]
    return url


def _resolve_database_url() -> str:
    # CURATWIN_DATABASE_URL is an explicit override that beats anything the
    # Vercel/Neon integration injects (used by tests and by local dev).
    for var in ("CURATWIN_DATABASE_URL", "DATABASE_URL", "POSTGRES_URL"):
        raw = os.environ.get(var, "").strip()
        if raw:
            return _normalize(raw)
    if IS_VERCEL:
        raise RuntimeError(
            "No database configured. Connect Vercel Postgres to this project "
            "so DATABASE_URL is injected."
        )
    return f"sqlite:///{os.path.join(BASE_DIR, 'curatwin.db')}"


DATABASE_URL = _resolve_database_url()
IS_SQLITE = DATABASE_URL.startswith("sqlite")

# Auto-DDL is for SQLite (local dev + tests) only. On Postgres the schema is
# created once, out of band, by scripts/init_db.py. Set AUTO_CREATE_TABLES=1
# in Vercel only as a one-shot escape hatch, then remove it.
AUTO_CREATE_TABLES = os.environ.get(
    "AUTO_CREATE_TABLES", "1" if IS_SQLITE else "0"
) == "1"

MODEL_STORE_PATH = os.path.join(BASE_DIR, "backend", "ai", "model_store")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
