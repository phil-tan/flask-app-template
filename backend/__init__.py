# init.py

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from flask_cors import CORS
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
    CORS(app)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    # app.app_context().push()
    # db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # Serve the React pages route here
    @app.route('/react', defaults={'path': ''})
    @app.route('/react/<path:path>')
    @login_required
    def serve_react_app(path):
        print('serving react')
        print(path)
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:filename>')
    def serve_root_files(filename):
        # Serve other root files directly from the build directory
        return send_from_directory(app.static_folder, filename)

    # pages_controller
    from .controllers.pages import pages
    app.register_blueprint(pages)

    # auth controller
    from .controllers.auth import auth
    app.register_blueprint(auth)

    from .controllers.api import api
    app.register_blueprint(api)

    from .controllers.cli import cli
    app.register_blueprint(cli)

    return app