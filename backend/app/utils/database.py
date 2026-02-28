from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'sqlite:///./sqlite.db' # URL

# create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': True}
)

# create session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base model
Base = declarative_base()

# db
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
