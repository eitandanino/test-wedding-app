import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///wedding.db'
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

