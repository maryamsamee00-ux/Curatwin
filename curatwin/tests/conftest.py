import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Force a throwaway SQLite file BEFORE backend.config is imported. pytest loads
# conftest.py ahead of every test module, so this ordering is guaranteed.
os.environ["CURATWIN_DATABASE_URL"] = (
    "sqlite:///" + os.path.join(tempfile.gettempdir(), "curatwin_test.db")
)
os.environ.setdefault("SECRET_KEY", "test-only-secret-key")
for leaked in ("DATABASE_URL", "POSTGRES_URL", "VERCEL", "AUTO_CREATE_TABLES"):
    os.environ.pop(leaked, None)

from backend.database import Base, engine  # noqa: E402

# Belt and braces: this suite calls drop_all(). Never let it near a real DB.
assert engine.url.get_backend_name() == "sqlite", (
    f"refusing to run destructive tests against {engine.url.get_backend_name()}"
)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


from fastapi.testclient import TestClient  # noqa: E402
from backend.main import app  # noqa: E402


client = TestClient(app)


def register_user(name="Test Student", email="test@university.edu", password="SecurePass123"):
    return client.post("/api/auth/register", json={
        "name": name, "email": email, "password": password,
        "confirm_password": password, "age_range": "21-24"
    })


def get_token(email="test@university.edu", password="SecurePass123"):
    res = client.post("/api/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
