from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite for testing; replace with PostgreSQL for production
SQLALCHEMY_DATABASE_URL = "sqlite:///./health_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for route injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
