from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('DataBAse CREATED')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Entry1234' # This is needed to enable POST requests
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # This sets the location of the database
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

app = create_app()