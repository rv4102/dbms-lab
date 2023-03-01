from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from . import requires_access_level
from .forms import RegisterPatient
from flask import flash, redirect, url_for

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

@routes.route('/login')
def login():
    return render_template('login.html')

@routes.route('/frontdesk')
def frontdesk():
    return render_template('frontdesk_dashboard.html')

@routes.route('/frontdesk/register', methods=['GET', 'POST'])
def frontdesk_register():
    # if(request.method == 'POST'):
    #     print(request.form)
    #     return render_template('frontdesk_register.html')
    # else:
    #     return render_template('frontdesk_register.html')

    form = RegisterPatient()
    if form.validate_on_submit():
        print("Form validated")
        print(form.name.data)
        print(form.address.data)
        print(form.age.data)
        print(form.contact_number.data)
        print(form.emergency_contact.data)
        flash(f'Successfully registered patient {form.name.data}', 'success')
        return redirect(url_for('routes.frontdesk'))
    return render_template('frontdesk_register.html', form=form)

@routes.route('/frontdesk/admit')
def frontdesk_admit():
    return render_template('frontdesk_admit.html')

@routes.route('/frontdesk/discharge')
def frontdesk_discharge():
    return render_template('frontdesk_discharge.html')


