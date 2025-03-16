from app import create_app, db  # Import create_app and db from your app
from app.models import User  # Import your User model

app = create_app()  # Create the app instance

with app.app_context():  # Push the app context to allow database operations
    # Check if admin user already exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.set_password('admin')  # Replace 'admin' with a secure password in production
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")
