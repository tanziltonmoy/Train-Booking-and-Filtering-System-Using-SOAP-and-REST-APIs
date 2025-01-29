import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Load database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///train_booking.db")

# Configure the database engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database(seed_data: bool = True):
    """
    Initialize the database by creating all tables. Optionally seed data.
    """
    try:
        logger.info("Creating tables in the database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
        
        if seed_data:
            logger.info("Seeding the database with random train data...")
            from utils.generate_trains import generate_random_trains_and_seats
            session = SessionLocal()
            generate_random_trains_and_seats(session, num_trains=50)
            session.close()
            logger.info("Database seeding completed successfully.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")

def get_db():
    """
    Provide a database session for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize the database with seeding enabled
    initialize_database(seed_data=True)
