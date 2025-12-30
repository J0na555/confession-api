from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Use absolute path to ensure database is always in the same location
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = BASE_DIR / "confessions.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# dependency to get the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()