from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import requires_access_level, mysql
from werkzeug.security import generate_password_hash
from .forms import *
from datetime import datetime
from .models import DE_Operator,Doctor,FD_Operator,Administrator, identify_class
from datetime import datetime, timedelta

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
    # get free rooms
    cur.execute("SELECT * FROM Room WHERE Room_Num NOT IN (SELECT Room_Num FROM Admitted)")
    free_rooms = cur.fetchall()
    # return render_template('frontdesk_dashboard.html',  total_patients = user = current_user)
    # return render_template('frontdesk_dashboard.html', patients=patients, admitted=admitted, discharged=discharged, user = current_user)
    return render_template('frontdesk_dashboard.html', total_patients=total_patients, admitted_patients=len(admitted), available_rooms = len(free_rooms), patients = patients, admitted_patients_list=admitted, user = current_user)  


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

@routes.route('/frontdesk/admit/<patient_id>',methods = ['GET','POST'])
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

@routes.route('/frontdesk/appointment_schedule')
def frontdesk_appointment_schedule():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID NOT IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_appointment_schedule.html', patients=patients,  user = current_user)

@routes.route('/frontdesk/appointment_schedule/<patient_id>', methods=['GET', 'POST'])
def frontdesk_appointment_schedule_patient(patient_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Doctor")
    doctors = cur.fetchall()
    cur.close()
    return render_template('frontdesk_appointment_schedule_patient.html', patient_id=patient_id, doctors=doctors,  user = current_user)

@routes.route('/frontdesk/appointment_schedule/<patient_id>/<doctor_id>', methods=['GET', 'POST'])
def frontdesk_appointment_schedule_date(patient_id, doctor_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        date_selected = request.form.get('date')
        cur.execute("SELECT Appointment_Time FROM Appointment WHERE Appointment_Date = %s AND Doctor_ID = %s", (date_selected, doctor_id))
        appointments = cur.fetchall()
        # print(appointments)
        print("\n\n\nAPPOINTMENTS\n\n\n", appointments)
        if(len(appointments) == 0):
            time_scheduled = '10:00:00'
            flash(f'Appointment scheduled for {date_selected} at {time_scheduled}', 'success')
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doctor_id, date_selected, time_scheduled))
            mysql.connection.commit()
        else:
            sorted_appointments = sorted(appointments)
            last_appointment_time = sorted_appointments[-1][0]
            print("TYPE LAST APP", type(last_appointment_time))
            last_appointment_time = str(last_appointment_time)
            # print("STR TIME",str_time)
            # print("\n\n\nLAST APPOINTMENT TIME\n\n\n", last_appointment_time)
            # print((last_appointment_time[0]))
            # last_appointment_time = datetime.strftime(last_appointment_time, '%H:%M:%S')
            # print(last_appointment_time)
            # check if last appointment is before 4pm
            # if(last_appointment_time.hour < 16):
            #     next_appointment_time = last_appointment_time + timedelta(minutes=60)
            #     flash(f'Appointment scheduled for {date_selected} at {next_appointment_time}', 'success')
            #     cur = mysql.connection.cursor()
            #     cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doctor_id, date_selected, next_appointment_time))
            #     mysql.connection.commit()
            # else:
            #     flash(f'No appointments available on {date_selected}', 'danger')
            if last_appointment_time < '16:00:00':
                next_appointment_time = datetime.strptime(last_appointment_time, '%H:%M:%S') + timedelta(minutes=60)
                next_appointment_time = datetime.strftime(next_appointment_time, '%H:%M:%S')
                flash(f'Appointment scheduled for {date_selected} at {next_appointment_time}', 'success')
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doctor_id, date_selected, next_appointment_time))
                mysql.connection.commit()
            else:
                flash(f'No appointments available on {date_selected}', 'danger')
        cur.close()
        return redirect(url_for('routes.frontdesk_appointment_schedule'))
    else:
        return render_template('frontdesk_appointment_schedule_date.html', patient_id=patient_id, doctor_id=doctor_id,  user = current_user)
    
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
        print(form.users.data, form.username.data)
        user = identify_class(form.users.data).get_by_username(form.username.data)
        if user:
            flash('Username already exists.', category='danger')
            return render_template('admin_add.html', form=form,  user=current_user)
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

@routes.route('/dataentry')
def dataentry():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Test_ID , TestDate,  Category , Patient.Name, BodyPart FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0")
    incomplete_tests = cur.fetchall()
    cur.execute("SELECT Test_ID , TestDate,  Category , Patient.Name, BodyPart , Result FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 1")
    complete_tests = cur.fetchall()
    cur.execute("SELECT Treatment_ID, TreatmentDate, Category, Details,Doctor.Name, Patient.Name FROM Treatment JOIN Patient JOIN Doctor where Treatment.Patient_ID = Patient.Patient_ID and Treatment.Doctor_ID = Doctor.Doctor_ID")
    treatments = cur.fetchall()
    cur.close()
    print(incomplete_tests, complete_tests, treatments)
    return render_template('dataentry_main_dashboard.html', incomplete_tests=incomplete_tests, complete_tests=complete_tests, treatments=treatments, user=current_user)

@routes.route('/dataentry/test')
def dataentry_test():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Test_ID , TestDate,  Category , Name, BodyPart FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0")
    tests = cur.fetchall()
    cur.close()
    return render_template('dataentry_select_test.html', user=current_user,tests = tests)

@routes.route('/dataentry/test/<test_id>', methods=['GET', 'POST'])
def dataentry_test_id(test_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT TestDate,  Category , BodyPart , Name  FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0 and Test.Test_ID = %s", (test_id,))
    test = cur.fetchone()
    cur.close()
    form = AddTestResult()
    if form.validate_on_submit():
        print("Form validated")
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE Test SET ResultObtained = 1 , Result = '{form.result.data}'WHERE Test_ID = '{test_id}'")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added test result {test[1]} for patient {test[3]}', 'success')
        return redirect(url_for('routes.dataentry'))
    return render_template('dataentry_add_test.html', user=current_user, test=test, form=form)

@routes.route('/dataentry/treatment')
def dataentry_select_patient():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Patient_ID,Name,Address,Age,Gender,Personal_Contact ,Emergency_Contact FROM Patient")
    patients = cur.fetchall()
    return render_template('dataentry_select_patient.html', user=current_user,patients = patients)

@routes.route('/dataentry/treatment/<patient_id>', methods=['GET', 'POST'])
def dataentry_select_doctor(patient_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Doctor_ID,Name,Username,Age,Gender,Personal_Contact FROM Doctor")
    doctors = cur.fetchall()
    print(doctors)
    return render_template('dataentry_select_doctor.html', user=current_user,doctors = doctors, patient_id = patient_id)

@routes.route('/dataentry/treatment/<patient_id>/<doctor_id>', methods=['GET', 'POST'])
def dataentry_treatment(patient_id, doctor_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name FROM Patient where Patient_ID = %s", (patient_id,))
    patient = cur.fetchone()
    cur.execute("SELECT Name FROM Doctor where Doctor_ID = %s", (doctor_id,))
    doctor = cur.fetchone()
    patient = patient[0]
    doctor = doctor[0]
    print(patient)
    print(doctor)
    cur.close()
    form = AddTreatment()
    if form.validate_on_submit():
        print("Form validated")
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO Treatment (Patient_ID, Doctor_ID, TreatmentDate, Category,Details) VALUES ('{patient_id}', '{doctor_id}', '{form.treatment_date.data}', '{form.category.data}', '{form.details.data}')")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added treatment {form.category.data} for patient {patient} by doctor {doctor}', 'success')
        return redirect(url_for('routes.dataentry'))
    return render_template('dataentry_add_treatment.html', user=current_user, patient=patient, doctor=doctor, form=form)