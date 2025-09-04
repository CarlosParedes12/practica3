import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse

def _normalize_db_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg2://", 1)
    return url

raw_url = os.getenv("DATABASE_URL", "").strip()  # <-- elimina espacios/saltos
if not raw_url:
    # fallback explícito para detectar si no llegó la env var
    raw_url = "postgresql+psycopg2://user:pass@localhost:5432/dbname"

DATABASE_URL = _normalize_db_url(raw_url)

# Log seguro para verificar a qué host/DB te conectas (sin user/pass)
try:
    parsed = urlparse(DATABASE_URL)
    print(f"[DB] dialect={parsed.scheme} host={parsed.hostname} db={parsed.path.lstrip('/')}")
except Exception as e:
    print(f"[DB] URL parse error: {e}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
