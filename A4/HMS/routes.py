from HMS import app
from flask import render_template

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




