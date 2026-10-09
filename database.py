from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# File-based SQLite database (created automatically in the project folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency: provides one DB session per request, then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
