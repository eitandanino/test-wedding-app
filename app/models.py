from flask_login import UserMixin

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):  # Inherit from UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='creator', lazy='dynamic')
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Add is_active (important!)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(9), unique=True, nullable=False)
    language = db.Column(db.String(10), default='he')
    groom_name = db.Column(db.String(100))
    groom_father_name = db.Column(db.String(100))
    groom_mother_name = db.Column(db.String(100))
    groom_last_name = db.Column(db.String(100))
    bride_name = db.Column(db.String(100))
    bride_father_name = db.Column(db.String(100))
    bride_mother_name = db.Column(db.String(100))
    bride_last_name = db.Column(db.String(100))
    wedding_date = db.Column(db.Date)  # Ensure this is a Date field
    reception_time = db.Column(db.String(10))  # Store as string (e.g., '14:30')
    wedding_time = db.Column(db.String(10))  # Store as string (e.g., '16:00')
    hebrew_wedding_date = db.Column(db.String(50))
    invitation_image = db.Column(db.String(200))
    hall_name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    waze_link = db.Column(db.String(200))
    template = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    responses = db.relationship('Response', backref='event', lazy='dynamic')


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    is_attending = db.Column(db.Boolean, default=False)
    num_guests = db.Column(db.Integer, nullable=True)
    is_vegetarian = db.Column(db.Boolean,)
    side = db.Column(db.String(10))  # 'groom' or 'bride'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    guest_status = db.Column(db.String(50), nullable=True)
    table_number = db.Column(db.Integer, nullable=True)
