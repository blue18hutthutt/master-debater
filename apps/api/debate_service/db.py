from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database file relative to project root
DATABASE_URL = "sqlite:///db/masterdebater.db"

# Required for SQLite multithreading in FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to use in FastAPI endpoints
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
