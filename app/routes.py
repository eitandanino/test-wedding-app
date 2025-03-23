import os
import pandas as pd
import xlsxwriter  # Add this import
from io import BytesIO
from datetime import datetime
from config import Config

from urllib.parse import quote

from flask import Blueprint, render_template, redirect, url_for, flash, current_app, send_file, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.utils import generate_random_link
from app.models import User, Event, Response, Guest
from app.forms import LoginForm, RegistrationForm, EventForm, ResponseForm

# Create a Blueprint for routes
bp = Blueprint('main', __name__)

# Access the Hebrew headers
HEBREW_HEADERS = Config.HEBREW_HEADERS
HEBREW_VALUES = Config.HEBREW_VALUES


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the server-side session
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.logout_page'))  # Redirect to the logout page


@bp.route('/logout_page')
def logout_page():
    return render_template('logout.html')  # Render the logout.html template


@bp.route('/dashboard')
@login_required
def dashboard():
    # Fetch all events created by the current user
    events = current_user.events.all()

    # Fetch responses for each event
    event_responses = []
    for event in events:
        responses = Response.query.filter_by(event_id=event.id).all()
        event_responses.append({
            'event': event,
            'responses': responses
        })

    return render_template('dashboard.html', event_responses=event_responses)


@bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Generate a unique link
        while True:
            link = generate_random_link()
            # Check if the link already exists in the database
            if not Event.query.filter_by(link=link).first():
                break  # Link is unique

        try:
            # Convert wedding_date to a date object
            wedding_date_obj = datetime.strptime(str(form.wedding_date.data), '%Y-%m-%d').date()

            # Create the event object
            event = Event(
                link=link,  # Add the unique link to the event
                language=form.language.data,
                groom_name=form.groom_name.data,
                groom_father_name=form.groom_father_name.data,
                groom_mother_name=form.groom_mother_name.data,
                groom_last_name=form.groom_last_name.data,
                bride_name=form.bride_name.data,
                bride_father_name=form.bride_father_name.data,
                bride_mother_name=form.bride_mother_name.data,
                bride_last_name=form.bride_last_name.data,
                wedding_date=wedding_date_obj,  # Use the date object
                hebrew_wedding_date=form.hebrew_wedding_date.data,
                reception_time=form.reception_time.data.strftime('%H:%M'),  # Format the time
                wedding_time=form.wedding_time.data.strftime('%H:%M'),  # Format the time
                hall_name=form.hall_name.data,
                address=form.address.data,
                waze_link=form.waze_link.data,
                template=form.template.data,
                user_id=current_user.id
            )

            # Handle file upload
            if form.invitation_image.data:
                file = form.invitation_image.data
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)  # Ensure the upload folder exists
                file_path = os.path.join(upload_folder, filename)

                try:
                    file.save(file_path)
                    event.invitation_image = filename  # Store ONLY the filename
                except Exception as e:
                    print(f"Error saving file: {e}")
                    flash('Error uploading image. Please try again.', 'error')
                    return render_template('create_event.html', form=form)

            # Save the event to the database
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.dashboard'))

        except ValueError as e:  # Catch the error if form.wedding_date is None or invalid
            print(f"Error processing form data: {e}")
            flash('Error in form data. Please check your inputs.', 'error')
            return render_template('create_event.html', form=form)

    return render_template('create_event.html', form=form)


@bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Ensure the current user is the creator of the event
    if event.user_id != current_user.id:
        flash('You do not have permission to edit this event.', 'error')
        return redirect(url_for('main.dashboard'))

    # Pre-fill the form with the event's data
    form = EventForm(obj=event)

    # Manually set the date and time fields to ensure proper formatting
    # form.wedding_date.data = event.wedding_date  # Already a date object
    # Manually set the date and time fields
    if request.method == 'GET':
        form.reception_time.data = datetime.strptime(event.reception_time, '%H:%M').time()
        form.wedding_time.data = datetime.strptime(event.wedding_time, '%H:%M').time()

    if form.validate_on_submit():
        try:
            # Update the event with the new data
            event.language = form.language.data
            event.groom_name = form.groom_name.data
            event.groom_father_name = form.groom_father_name.data
            event.groom_mother_name = form.groom_mother_name.data
            event.groom_last_name = form.groom_last_name.data
            event.bride_name = form.bride_name.data
            event.bride_father_name = form.bride_father_name.data
            event.bride_mother_name = form.bride_mother_name.data
            event.bride_last_name = form.bride_last_name.data

            # Convert wedding_date to a date object
            event.wedding_date = form.wedding_date.data  # Already a date object

            # Convert reception_time and wedding_time to time strings
            event.reception_time = form.reception_time.data.strftime('%H:%M')
            event.wedding_time = form.wedding_time.data.strftime('%H:%M')

            event.hebrew_wedding_date = form.hebrew_wedding_date.data
            event.hall_name = form.hall_name.data
            event.address = form.address.data
            event.waze_link = form.waze_link.data
            event.template = form.template.data

            # Handle file upload
            if form.invitation_image.data:
                file = form.invitation_image.data
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                event.invitation_image = filename  # Update the image filename

            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            print(f"Error updating event: {e}")
            flash('Error updating event. Please try again.', 'error')
            return render_template('edit_event.html', form=form, event=event)

    return render_template('edit_event.html', form=form, event=event)


@bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Check if the current user is the creator of the event
    if event.user_id != current_user.id:
        flash('You are not authorized to delete this event.', 'error')
        return redirect(url_for('main.dashboard'))

    # Delete the associated invitation image
    if event.invitation_image:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], event.invitation_image)
        try:
            os.remove(image_path)
        except FileNotFoundError:
            pass  # Ignore if the file doesn't exist

    # Delete responses associated with the event
    for response in event.responses:
        db.session.delete(response)

    # Delete the event itself
    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/response/delete/<int:response_id>', methods=['POST'])
def delete_response(response_id):
    response = Response.query.get_or_404(response_id)
    db.session.delete(response)
    db.session.commit()
    flash('Guest deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/responses/delete', methods=['POST'])
def delete_multiple_responses():
    response_ids = request.form.getlist('response_ids')
    if response_ids:
        for response_id in response_ids:
            response = Response.query.get(int(response_id))
            if response:
                db.session.delete(response)
        db.session.commit()
        flash('Selected guests deleted successfully.', 'success')
    else:
        flash('No guests selected to delete.', 'warning')
    return redirect(url_for('main.dashboard'))


@bp.route('/invitation/<string:link>', methods=['GET', 'POST'])
def invitation(link):
    event = Event.query.filter_by(link=link).first_or_404()
    form = ResponseForm()

    # Generate Google Calendar link
    start_time = datetime.strptime(f"{event.wedding_date} {event.reception_time}", "%Y-%m-%d %H:%M")
    google_calendar_link = (
        "https://www.google.com/calendar/render?action=TEMPLATE"
        f"&text={quote(f'החתונה של {event.groom_name} ו{event.bride_name}')}"
        f"&dates={start_time.strftime('%Y%m%dT%H%M%S')}"
        f"&details={quote('בואו לחגוג עמנו בחתונה')}"
        f"&location={quote(event.address)}"
        "&sf=true&output=xml"
    )

    if form.validate_on_submit():
        if form.is_attending.data == 'no':
            num_guests = None
            is_vegetarian = None
            side = None
        else:
            num_guests = form.num_guests.data
            is_vegetarian = (form.is_vegetarian.data == 'yes')
            side = form.side.data

        response = Response(
            guest_name=form.guest_name.data,
            phone_number=form.phone_number.data,
            is_attending=(form.is_attending.data == 'yes'),
            num_guests=num_guests,
            is_vegetarian=is_vegetarian,
            side=side,
            event_id=event.id
        )
        db.session.add(response)
        db.session.commit()
        flash('Response submitted successfully!', 'success')
        return redirect(url_for('main.invitation', link=link))
    return render_template('invitation.html', event=event, form=form, google_calendar_link=google_calendar_link)


@bp.route('/admin')
@login_required
def admin():
    # Ensure the current user is an admin
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'error')
        return redirect(url_for('main.dashboard'))

    # Fetch all users and events for the admin panel
    users = User.query.all()
    events = Event.query.all()

    return render_template('admin.html', users=users, events=events)


@bp.route('/admin/event/<int:event_id>')
@login_required
def admin_event_responses(event_id):
    # Ensure the current user is an admin
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.dashboard'))

    # Fetch the event and its responses
    event = Event.query.get_or_404(event_id)
    responses = Response.query.filter_by(event_id=event.id).all()

    return render_template('admin_event_responses.html', event=event, responses=responses)


@bp.route('/export_responses/<int:event_id>', methods=['POST'])
@login_required
def export_responses(event_id):
    event = Event.query.get_or_404(event_id)
    responses = Response.query.filter_by(event_id=event.id).all()

    # Create a DataFrame from the responses
    data = {
        'Guest Name': [r.guest_name for r in responses],
        'Phone Number': [r.phone_number for r in responses],
        'Attending': [HEBREW_VALUES['Yes'] if r.is_attending else HEBREW_VALUES['No'] for r in responses],
        'Number of Guests': [r.num_guests for r in responses],
        'Vegetarian': [HEBREW_VALUES['Yes'] if r.is_vegetarian else HEBREW_VALUES['No'] for r in responses],
        'Side': [HEBREW_VALUES[r.side] if r.side is not None else '' for r in responses],
        'Guest Status': [r.guest_status for r in responses],  # New field
        'Table Number': [r.table_number for r in responses]  # New field
    }
    df = pd.DataFrame(data)

    # Rename columns to Hebrew headers
    df.rename(columns=HEBREW_HEADERS, inplace=True)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Responses', index=False)
    output.seek(0)

    # Send the file as a response
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'{event.groom_name}_{event.bride_name}_responses.xlsx'
    )


@bp.route('/upload_guest_list/<int:event_id>', methods=['POST'])
@login_required
def upload_guest_list(event_id):
    if 'guest_list' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('main.dashboard'))

    file = request.files['guest_list']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('main.dashboard'))

    try:
        # Read the Excel file
        df = pd.read_excel(file)
        
        # Reverse the Hebrew headers to English for internal processing
        reverse_headers = {v: k for k, v in HEBREW_HEADERS.items()}
        df.rename(columns=reverse_headers, inplace=True)
        
        # Validate required columns
        if 'Guest Name' not in df.columns or 'Phone Number' not in df.columns:
            flash('Invalid file format. Missing required columns.', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Save the uploaded guest list to the database
        event = Event.query.get_or_404(event_id)
        
        # First, delete any existing guests for this event to avoid duplicates
        Guest.query.filter_by(event_id=event_id).delete()
        
        # Add new guests from the uploaded file
        for index, row in df.iterrows():
            guest = Guest(
                guest_name=row['Guest Name'],
                phone_number=str(row['Phone Number']),
                event_id=event_id
            )
            db.session.add(guest)
        
        db.session.commit()
        flash('Guest list saved to database successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        flash(f'Error processing the uploaded file: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))


@bp.route('/download_template')
@login_required
def download_template():
    # Create a template Excel file
    data = {
        'Guest Name': [],
        'Phone Number': [],
    }
    df = pd.DataFrame(data)

    # Rename columns to Hebrew headers
    df.rename(columns=HEBREW_HEADERS, inplace=True)

    # Save the template to a BytesIO object
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Send the file as a response
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='guest_list_template.xlsx'
    )

# Add these imports at the top of the file
import pandas as pd
from app.utils import send_sms

# Add these routes after the existing admin routes

@bp.route('/admin/send_sms/<int:event_id>', methods=['GET', 'POST'])
@login_required
def admin_send_sms(event_id):
    # Ensure the current user is an admin
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.dashboard'))
    
    event = Event.query.get_or_404(event_id)
    responses = Response.query.filter_by(event_id=event.id).all()
    
    if request.method == 'POST':
        message = request.form.get('message')
        selected_guests = request.form.getlist('selected_guests')
        
        if not message:
            flash('Please enter a message to send.', 'error')
            return redirect(url_for('main.admin_send_sms', event_id=event_id))
        
        success_count = 0
        error_count = 0
        
        for guest_id in selected_guests:
            guest = Response.query.get(int(guest_id))
            if guest and guest.phone_number:
                # Replace placeholders in the message
                personalized_message = message.replace('{name}', guest.guest_name)
                personalized_message = personalized_message.replace('{event}', f"{event.groom_name} & {event.bride_name}")
                
                # Send the SMS
                result = send_sms(guest.phone_number, personalized_message)
                
                if result.get('success', False):
                    success_count += 1
                else:
                    error_count += 1
        
        if success_count > 0:
            flash(f'Successfully sent {success_count} SMS messages.', 'success')
        if error_count > 0:
            flash(f'Failed to send {error_count} SMS messages.', 'error')
            
        return redirect(url_for('main.admin_event_responses', event_id=event_id))
    
    return render_template('admin_send_sms.html', event=event, responses=responses)


@bp.route('/admin/bulk_sms/<int:event_id>', methods=['POST'])
@login_required
def admin_bulk_sms(event_id):
    # Ensure the current user is an admin
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.dashboard'))
    
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        message = request.form.get('message')
        send_to = request.form.get('send_to', 'all')
        
        if not message:
            flash('Please enter a message to send.', 'error')
            return redirect(url_for('main.admin_send_sms', event_id=event_id))
        
        # Get the appropriate guests based on the selection
        if send_to == 'all':
            guests = Response.query.filter_by(event_id=event.id).all()
        elif send_to == 'attending':
            guests = Response.query.filter_by(event_id=event.id, is_attending=True).all()
        elif send_to == 'not_attending':
            guests = Response.query.filter_by(event_id=event.id, is_attending=False).all()
        elif send_to == 'not_responded':
            # This requires more complex logic - get all phone numbers from the guest list
            # that don't have a response
            # For simplicity, we'll skip this implementation for now
            flash('Sending to non-responded guests is not implemented yet.', 'error')
            return redirect(url_for('main.admin_send_sms', event_id=event_id))
        else:
            guests = []
        
        success_count = 0
        error_count = 0
        
        for guest in guests:
            if guest.phone_number:
                # Replace placeholders in the message
                personalized_message = message.replace('{name}', guest.guest_name)
                personalized_message = personalized_message.replace('{event}', f"{event.groom_name} & {event.bride_name}")
                
                # Send the SMS
                result = send_sms(guest.phone_number, personalized_message)
                
                if result.get('success', False):
                    success_count += 1
                else:
                    error_count += 1
        
        if success_count > 0:
            flash(f'Successfully sent {success_count} SMS messages.', 'success')
        if error_count > 0:
            flash(f'Failed to send {error_count} SMS messages.', 'error')
            
        return redirect(url_for('main.admin_event_responses', event_id=event_id))
    
    return redirect(url_for('main.admin_send_sms', event_id=event_id))


@bp.route('/delete_guest/<int:guest_id>', methods=['POST'])
@login_required
def delete_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    event = Event.query.get(guest.event_id)
    
    # Check if the current user is authorized to delete this guest
    if event.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this guest.', 'error')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(guest)
    db.session.commit()
    flash('Guest deleted successfully.', 'success')
    return redirect(url_for('main.view_guest_list', event_id=event.id))


@bp.route('/download_comparison/<int:event_id>', methods=['GET'])
@login_required
def download_comparison(event_id):
    # Get the event
    event = Event.query.get_or_404(event_id)
    
    # Check if the current user is authorized to access this event
    if event.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to access this event.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Create a comparison Excel file
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    # Add headers
    headers = ['Guest Name', 'Phone Number', 'Attending', 'Number of Guests', 'Vegetarian', 'Side']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Get responses for this event
    responses = Response.query.filter_by(event_id=event.id).all()
    
    # Write data
    for row, response in enumerate(responses, start=1):
        worksheet.write(row, 0, response.guest_name)
        worksheet.write(row, 1, response.phone_number)
        worksheet.write(row, 2, 'Yes' if response.is_attending else 'No')
        worksheet.write(row, 3, response.num_guests or 0)
        worksheet.write(row, 4, 'Yes' if response.is_vegetarian else 'No')
        worksheet.write(row, 5, response.side or 'N/A')
    
    workbook.close()
    output.seek(0)
    
    # Generate filename
    filename = f"comparison_{event.groom_name}_{event.bride_name}.xlsx"
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@bp.route('/view_guest_list/<int:event_id>')
@login_required
def view_guest_list(event_id):
    # Get the event
    event = Event.query.get_or_404(event_id)
    
    # Check if the current user is authorized to access this event
    if event.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to access this event.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get all guests for this event
    guests = Guest.query.filter_by(event_id=event.id).all()
    
    return render_template('view_guest_list.html', event=event, guests=guests)
