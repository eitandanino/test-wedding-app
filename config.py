import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://default-url')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'he'  # Default language is Hebrew
    UPLOAD_FOLDER = 'app/static/uploads'

    # Hebrew headers mapping
    HEBREW_HEADERS = {
        'Guest Name': 'שם',
        'Phone Number': 'טלפון',
        'Attending': 'משתתף',
        'Number of Guests': 'מספר אורחים',
        'Vegetarian': 'צמחוני',
        'Side': 'צד',
        'Responded': 'הגיב',
        'Normalized Phone Number': 'מספר טלפון מנורמל',
    }

    HEBREW_VALUES = {
        'Yes': 'כן',
        'No': 'לא',
        'groom': 'חתן',
        'bride': 'כלה',
    }

