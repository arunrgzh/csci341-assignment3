import os


class Config:
    """Application configuration"""
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:ZIFA0PI6fwmQlbjmPbEMC6QHGAJeq8is@dpg-d4iuqe95pdvs7385o020-a.oregon-postgres.render.com/caregivers",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Flask configuration
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

