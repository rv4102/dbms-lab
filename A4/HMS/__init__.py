from flask import Flask, sessions
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import session, redirect, url_for
from functools import wraps

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
    app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_USER'] = 'shivam'
    # app.config['MYSQL_PASSWORD'] = 'Aniket'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'hospital_db'

    mysql.init_app(app)

    from .models import Administrator, Doctor, DE_Operator, FD_Operator

    # bcrypt = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        for staff in [Administrator, Doctor, DE_Operator, FD_Operator]:
            user = staff.get(id)
            if user:
                return user

    return app

def requires_access_level(access_level):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if session['Access_Level'] != access_level:
                    return redirect(url_for('routes.index', message="You do not have access to that page. Sorry!"))
                return f(*args, **kwargs)
            return decorated_function
        return decorator


