from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from . import requires_access_level
from .forms import RegisterPatient
from flask import flash, redirect, url_for
from . import mysql
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
def login():
    return render_template('login.html', user = current_user)

@routes.route('/patients')
@login_required
@requires_access_level(1)
def patients():
    return render_template('patients.html', user = current_user)

@routes.route('/doctors')
@login_required
@requires_access_level(2)
def doctors():
    return render_template('doctors.html', user = current_user)

@routes.route('/appointments')
@login_required
@requires_access_level(2)
def appointments():
    return render_template('appointments.html', user = current_user)

@routes.route('/tests')
@login_required
@requires_access_level(3)
def tests():
    return render_template('tests.html' ,user = current_user)

@routes.route('/admissions')
@login_required
@requires_access_level(4)
def admissions():
    return render_template('admissions.html',  user = current_user)

@routes.route('/index')
@login_required
def index():
    return render_template('index.html', user = current_user)

@routes.route('/frontdesk')
def frontdesk():
    return render_template('frontdesk_dashboard.html',  user = current_user)

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
        print(form.gender.data)
        print(form.contact_number.data)
        print(form.emergency_contact.data)
        flash(f'Successfully registered patient {form.name.data}', 'success')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Patient (Name, Address, Age, Gender, Personal_Contact, Emergency_Contact) VALUES (%s, %s, %s, %s, %s, %s)", (form.name.data, form.address.data, form.age.data, form.gender.data, form.contact_number.data, form.emergency_contact.data))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('routes.frontdesk_register'))
    return render_template('frontdesk_register.html', form=form,  user = current_user)

@routes.route('/frontdesk/admit')
def frontdesk_admit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID NOT IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_admit.html', patients=patients,  user = current_user)
    # return render_template('frontdesk_admit.html')

@routes.route('/frontdesk/admit/<patient_id>')
def frontdesk_admit_patient(patient_id):
    print(patient_id)
    cur = mysql.connection.cursor()
    date = datetime.now().strftime("%Y-%m-%d")

    cur.execute("SELECT Room_Num FROM Room WHERE Room_Num NOT IN (SELECT Room_Num FROM Admitted)")
    room_number = cur.fetchone()
    if room_number is None:
        flash(f'No rooms available', 'danger')
        return redirect(url_for('routes.frontdesk_admit'))
    flash(f'Patient admitted to room {room_number[0]}', 'success')
    cur.execute("INSERT INTO Admitted (Patient_ID, Room_Num, Date_Admitted) VALUES (%s, %s, %s)", (patient_id, room_number, date))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('routes.frontdesk_admit'))

@routes.route('/frontdesk/discharge')
def frontdesk_discharge():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_discharge.html', patients=patients,  user = current_user)
    # return render_t/emplate('frontdesk_discharge.html')

@routes.route('/frontdesk/discharge/<patient_id>')
def frontdesk_discharge_patient(patient_id):
    print(patient_id)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Admitted WHERE Patient_ID = %s", (patient_id,))
    mysql.connection.commit()
    cur.close()
    flash(f'Patient discharged', 'success')
    return redirect(url_for('routes.frontdesk_discharge'))


