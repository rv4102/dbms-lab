from flask import render_template, Blueprint
from flask_login import login_required, current_user
from . import requires_access_level

routes = Blueprint('routes', __name__)

@routes.route('/')
@login_required
def index():
    return render_template('index.html')

@routes.route('/patients')
@login_required
@requires_access_level(1)
def patients():
    return render_template('patients.html')

@routes.route('/doctors')
@login_required
@requires_access_level(2)
def doctors():
    return render_template('doctors.html')

@routes.route('/appointments')
@login_required
@requires_access_level(2)
def appointments():
    return render_template('appointments.html')

@routes.route('/tests')
@login_required
@requires_access_level(3)
def tests():
    return render_template('tests.html')

@routes.route('/admissions')
@login_required
@requires_access_level(4)
def admissions():
    return render_template('admissions.html')




