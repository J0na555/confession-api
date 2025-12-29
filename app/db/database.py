from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="sqlite:///./confessions.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
sessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
{"check_same_thread": False}

# dependency to get the db session
def get_db():
    db=sessionLocal
    try:
        yield db
    finally:
        db.close()