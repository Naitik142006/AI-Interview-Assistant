# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")