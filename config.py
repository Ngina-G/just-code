import os


class Config:
    """General configuration parent class
    """
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Postgres@localhost/justcode'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST ='app/static/photos'

#  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

   
    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    """Production configuration child class

    Args:
        Config (The parent configuration class): with General production configuration settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Postgres@localhost/justcode'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
    DEBUG =True
    WTF_CSRF_SECRET_KEY="a csrf secret key" 


class Testconfig(Config):
    """Test configuration child class

    Args:
        Config (The parent configuration class): with General test configuration settings
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Postgres@localhost/justcode_test'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)


class DevConfig(Config):
    """Devlopment configuration child class

    Args:
        Config (the parent configuration class): with General configuration settngs
    """
    pass

    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:Postgres@localhost/justcode'
    # WTF_CSRF_SECRET_KEY="a csrf secret key" 
    # DEBUG =True



config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    'test':Testconfig
}