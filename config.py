import os


class Config:
    """Application configuration"""
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:Aarukow4171@localhost:5432/caregivers",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Flask configuration
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

