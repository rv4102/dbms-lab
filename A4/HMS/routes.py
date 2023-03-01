from flask import render_template, Blueprint, request

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

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/frontdesk')
def frontdesk():
    return render_template('frontdesk_dashboard.html')

@routes.route('/frontdesk/register', methods=['GET', 'POST'])
def frontdesk_register():
    if(request.method == 'POST'):
        print(request.form)
        return render_template('frontdesk_register.html')
    else:
        return render_template('frontdesk_register.html')


@routes.route('/frontdesk/admit')
def frontdesk_admit():
    return render_template('frontdesk_admit.html')

@routes.route('/frontdesk/discharge')
def frontdesk_discharge():
    return render_template('frontdesk_discharge.html')


