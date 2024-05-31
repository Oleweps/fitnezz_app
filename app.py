from flask import Flask
from flask_login import LoginManager
from config import Config
from project.extensions import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__, template_folder='project/templates', static_folder='project/static')
    app.config.from_object(config_class)
    
    migrate = Migrate(app, db)
    
    # Initialize Flask extensions here
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from project.models.test import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Initialize Flask extensions here

    # Register blueprints here
    from project.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from project.feature import bp as feature_bp
    app.register_blueprint(feature_bp)
    
    from project.api import bp as api_bp
    app.register_blueprint(api_bp)
    

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app