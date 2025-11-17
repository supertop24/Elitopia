from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
import stripe
import os
from app.config import Config

# Optional: only for local development
from dotenv import load_dotenv
if os.path.exists(".env"):
    load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Enable CORS
    CORS(app, supports_credentials=True, origins=["https://elite-emporium-omega.vercel.app/"])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)

    # Initialize Stripe
    stripe.api_key = os.environ.get("STRIPE_API_KEY")

    # Import models for migrations
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes/blueprints
    from .routes import register_routes
    register_routes(app)

    return app

# Expose app for WSGI servers or Vercel
app = create_app()
