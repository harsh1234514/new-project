"""
Database initialization script
Creates tables and seeds initial data
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from database import Base
from models import User
from auth_utils import get_password_hash

load_dotenv()

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/kpa_forms"
)

def init_database():
    """Initialize database with tables and seed data."""
    print("Initializing database...")
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if default user exists
        default_phone = os.getenv("DEFAULT_PHONE", "7760873976")
        existing_user = db.query(User).filter(User.phone_number == default_phone).first()
        
        if not existing_user:
            # Create default user
            default_password = os.getenv("DEFAULT_PASSWORD", "to_share@123")
            hashed_password = get_password_hash(default_password)
            
            default_user = User(
                phone_number=default_phone,
                password_hash=hashed_password,
                full_name="Test User",
                email="testuser@example.com"
            )
            
            db.add(default_user)
            db.commit()
            print(f"Default user created with phone: {default_phone}")
        else:
            print("Default user already exists")
            
    except Exception as e:
        print(f"Error creating default user: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Database initialization completed!")

if __name__ == "__main__":
    init_database()