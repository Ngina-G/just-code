from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import config_options
from flask_mail import Mail
from flask_simplemde import SimpleMDE


#Initializing Application and Initializing Flask Extensions
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
csrf = CSRFProtect()
mail = Mail()
simple = SimpleMDE()


def create_app(config_name):
    """Creating app configurations
        Initializing flask extensions
        Registering the blueprint
        setting Config
        Adds the views and forms
    """

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)


    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    simple.init_app(app)

    with app.app_context():
        db.create_all()

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    configure_uploads(app, photos)


    return app