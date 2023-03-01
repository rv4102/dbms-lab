from flask import Flask
# from flask_mysqldb import MySQL
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_session import Session
# from flask import render_template


# init MYSQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'hospital_db'

# mysql = MySQL(app)

# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

    from .routes import routes

    app.register_blueprint(routes, url_prefix='/')
    
    return app


