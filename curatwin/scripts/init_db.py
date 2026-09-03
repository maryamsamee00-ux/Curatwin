"""One-off schema bootstrap.

Run from the curatwin directory against the unpooled Neon URL:

    # PowerShell
    $env:CURATWIN_DATABASE_URL = "<DATABASE_URL_UNPOOLED>"
    $env:SECRET_KEY = "anything-nonempty"
    python scripts/init_db.py --yes
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect  # noqa: E402
from backend.database import engine, init_db  # noqa: E402


def main() -> int:
    print("Target:", engine.url.render_as_string(hide_password=True))
    if "--yes" not in sys.argv:
        if input("Create missing tables? [y/N] ").strip().lower() != "y":
            print("Aborted.")
            return 1
    init_db()
    print("Tables now present:", sorted(inspect(engine).get_table_names()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
