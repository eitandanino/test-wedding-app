from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, \
    TimeField, FileField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length, Regexp


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EventForm(FlaskForm):
    language = SelectField('Language', choices=[('he', 'Hebrew'), ('en', 'English')], default='he')
    groom_name = StringField('Groom Name', validators=[DataRequired()])
    groom_father_name = StringField('Groom Father Name', validators=[DataRequired()])
    groom_mother_name = StringField('Groom Mother Name', validators=[DataRequired()])
    groom_last_name = StringField('Groom Last Name', validators=[DataRequired()])
    bride_name = StringField('Bride Name', validators=[DataRequired()])
    bride_father_name = StringField('Bride Father Name', validators=[DataRequired()])
    bride_mother_name = StringField('Bride Mother Name', validators=[DataRequired()])
    bride_last_name = StringField('Bride Last Name', validators=[DataRequired()])
    wedding_date = DateField('Wedding Date', format='%Y-%m-%d', validators=[DataRequired()])
    hebrew_wedding_date = StringField('Hebrew Wedding Date', validators=[Optional()])
    reception_time = TimeField('Reception Time', format='%H:%M', validators=[DataRequired()])
    wedding_time = TimeField('Wedding Time', format='%H:%M', validators=[DataRequired()])
    invitation_image = FileField('Invitation Image', validators=[Optional()])
    hall_name = StringField('Hall Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    waze_link = StringField('Waze Link', validators=[DataRequired()])
    template = SelectField('Template', choices=[('template1', 'Template 1'), ('template2', 'Template 2')])
    submit = SubmitField('Create Event')


class ResponseForm(FlaskForm):
    guest_name = StringField('Guest Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number',
                               validators=[DataRequired(),
                                           Length(min=10, max=10, message='Phone number must be exactly 10 digits.'),
                                           Regexp(r'^\d{10}$', message='Phone number must contain only digits.'),
                                           ])
    is_attending = RadioField('Are you attending?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    num_guests = IntegerField('Number of Guests', validators=[Optional()])
    is_vegetarian = RadioField('Vegetarian Meal?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[Optional()])
    side = SelectField('Side', choices=[('groom', 'Groom Side'), ('bride', 'Bride Side')], validators=[Optional()])
    submit = SubmitField('Submit Response')
