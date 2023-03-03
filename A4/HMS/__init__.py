from flask import Flask, sessions, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask import session, redirect, url_for
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()
mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # init MYSQL

    # app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = 'hospital_db'

    mysql.init_app(app)

    from .models import Administrator, Doctor, DE_Operator, FD_Operator
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        print(id, "HELLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        id = str(id)
        type = id[0]
        print(id[1:])
        id = int(id[1:])
        if type == '1':
            return Administrator.get(id)
        elif type == '2':
            return Doctor.get(id)
        elif type == '3':
            return FD_Operator.get(id)
        elif type == '4':
            return DE_Operator.get(id)
        else:
            return None

    return app

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session['Access_Level'] != access_level:
                flash('You do not have access to that page. Sorry!', category='danger')
                return redirect(url_for('routes.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


