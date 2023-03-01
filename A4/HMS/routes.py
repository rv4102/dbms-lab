from flask import render_template, Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/patients')
def patients():
    return render_template('patients.html')

@routes.route('/doctors')
def doctors():
    return render_template('doctors.html')

@routes.route('/appointments')
def appointments():
    return render_template('appointments.html')

@routes.route('/tests')
def tests():
    return render_template('tests.html')

@routes.route('/admissions')
def admissions():
    return render_template('admissions.html')




