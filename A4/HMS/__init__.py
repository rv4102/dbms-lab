from flask import Flask
# from flask_mysqldb import MySQL
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_session import Session
from flask import render_template

app = Flask(__name__)

# init MYSQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'hospital_db'

Session(app)

# mysql = MySQL(app)

# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)


# routing
# 127.0.0.1/5000/   
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/tests')
def tests():
    return render_template('tests.html')

@app.route('/admissions')
def admissions():
    return render_template('admissions.html')

