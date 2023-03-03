from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import requires_access_level, mysql
from werkzeug.security import generate_password_hash
from .forms import *
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
def login():
    return render_template('login.html', user=current_user)

@routes.route('/patients')
@login_required
@requires_access_level(1)
def patients():
    return render_template('patients.html', user=current_user)

@routes.route('/doctors')
@login_required
@requires_access_level(2)
def doctors():
    return render_template('doctors.html', user=current_user)

@routes.route('/appointments')
@login_required
@requires_access_level(2)
def appointments():
    return render_template('appointments.html', user=current_user)

@routes.route('/tests')
@login_required
@requires_access_level(3)
def tests():
    return render_template('tests.html' ,user=current_user)

@routes.route('/admissions')
@login_required
@requires_access_level(4)
def admissions():
    return render_template('admissions.html',  user=current_user)

@routes.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)

@routes.route('/frontdesk')
def frontdesk():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient ORDER BY Patient_ID DESC LIMIT 5")
    patients = cur.fetchall()
    total_patients = len(patients)
    cur.execute("SELECT * FROM Admitted")
    admitted = cur.fetchall()
    cur.execute("SELECT * FROM Discharged")
    discharged = cur.fetchall()
    # return render_template('frontdesk_dashboard.html',  total_patients = user=current_user)
    # return render_template('frontdesk_dashboard.html', patients=patients, admitted=admitted, discharged=discharged, user=current_user)
    return render_template('frontdesk_dashboard.html', total_patients=total_patients, admitted_patients=len(admitted), patients = patients, admitted_patients_list=admitted, user=current_user)  


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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Patient (Name, Address, Age, Gender, Personal_Contact, Emergency_Contact) VALUES (%s, %s, %s, %s, %s, %s)", (form.name.data, form.address.data, form.age.data, form.gender.data, form.contact_number.data, form.emergency_contact.data))
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully registered patient {form.name.data}', 'success')
        return redirect(url_for('routes.frontdesk_register'))
    return render_template('frontdesk_register.html', form=form,  user=current_user)

@routes.route('/frontdesk/admit')
def frontdesk_admit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID NOT IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_admit.html', patients=patients,  user=current_user)

@routes.route('/frontdesk/admit/<patient_id>',methods = ['POST'])
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
    return render_template('frontdesk_discharge.html', patients=patients,  user=current_user)

@routes.route('/frontdesk/discharge/<patient_id>')
def frontdesk_discharge_patient(patient_id):
    print(patient_id)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Admitted WHERE Patient_ID = %s", (patient_id,))
    mysql.connection.commit()
    cur.close()
    flash(f'Patient discharged', 'success')
    return redirect(url_for('routes.frontdesk_discharge'))

@routes.route('/admin')
@login_required
@requires_access_level(1)
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Doctor_ID, Name, Address, Age, Gender, Personal_Contact FROM Doctor ORDER BY Doctor_ID LIMIT 5")
    doctors = cur.fetchall()
    cur.execute("SELECT FD_Operator_ID, Name, Address, Age, Gender, Personal_Contact FROM FD_Operator ORDER BY FD_Operator_ID LIMIT 5")
    fdos = cur.fetchall()
    cur.execute("SELECT DE_Operator_ID, Name, Address, Age, Gender, Personal_Contact FROM DE_Operator ORDER BY DE_Operator_ID LIMIT 5")
    deos = cur.fetchall()
    return render_template('admin_dashboard.html', total_doctors=len(doctors), total_fdo=len(fdos), total_deo=len(deos), doctors=doctors, fdos=fdos, deos=deos, user=current_user)

@routes.route('/admin/add', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_add():
    form = AddUser()
    if form.validate_on_submit():
        print("Form validated")
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO {form.users.data} (Username, Password, Name, Address, Age, Gender, Personal_Contact) VALUES ('{form.username.data}', '{generate_password_hash(form.password1.data, method='sha256')}', '{form.name.data}', '{form.address.data}', '{form.age.data}', '{form.gender.data}', '{form.contact_number.data}')")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added user {form.name.data}', 'success')
        return redirect(url_for('routes.admin_add'))
    # else:
    #     flash(f'Error adding user {form.name.data}', 'danger')
    
    return render_template('admin_add.html', form=form,  user=current_user)

@routes.route('/admin/delete', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_delete_select():
    form = DeleteUser()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT {form.users.data}_ID, Name, Address, Age, Gender, Personal_Contact FROM {form.users.data}")
        user_type_list = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('admin_delete.html', user_type=form.users.data, user_type_list=user_type_list, user=current_user)

    return render_template('admin_delete_select.html', form=form,  user=current_user)
    
@routes.route('/admin/delete/<user_type>/<user_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_delete_user(user_type, user_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM {user_type} WHERE {user_type}_ID = '{user_id}'")
    mysql.connection.commit()
    cur.close()
    flash(f'Successfully deleted {user_type} with ID {user_id}', 'success')
    return redirect(url_for('routes.admin_delete_select'))