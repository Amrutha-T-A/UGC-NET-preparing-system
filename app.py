from flask import Flask
from config import Config
from models import db, Admin, User
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "admin_login"  # Redirect unauthorized users to admin login

@login_manager.user_loader
def load_user(user_id):
    """Load user session by ID (supports Admin login only)"""
    return Admin.query.get(int(user_id))  # Modify if user login is added later

# Create all tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
from routes import *  # Import all routes
