from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import requires_access_level, mysql
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .forms import *
from datetime import datetime
from .models import DE_Operator,Doctor,FD_Operator,Administrator, identify_class
from datetime import datetime, timedelta
import os  
routes = Blueprint('routes', __name__)

@routes.route('/')
def login():
    return render_template('login.html', user=current_user)

@routes.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user)

@routes.route('/frontdesk')
@routes.route('/frontdesk/')
@login_required
@requires_access_level(3)
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
@routes.route('/frontdesk/register/', methods=['GET', 'POST'])
@login_required
@requires_access_level(3)
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
@routes.route('/frontdesk/admit/')
@login_required
@requires_access_level(3)
def frontdesk_admit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID NOT IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_admit.html', patients=patients,  user=current_user)

@routes.route('/frontdesk/admit/<patient_id>',methods = ['GET','POST'])
@routes.route('/frontdesk/admit/<patient_id>/',methods = ['GET','POST'])
@login_required
@requires_access_level(3)
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
@routes.route('/frontdesk/discharge/')
@login_required
@requires_access_level(3)
def frontdesk_discharge():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_discharge.html', patients=patients,  user=current_user)

@routes.route('/frontdesk/discharge/<patient_id>')
@routes.route('/frontdesk/discharge/<patient_id>/')
@login_required
@requires_access_level(3)
def frontdesk_discharge_patient(patient_id):
    print(patient_id)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Admitted WHERE Patient_ID = %s", (patient_id,))
    mysql.connection.commit()
    cur.close()
    flash(f'Patient discharged', 'success')
    return redirect(url_for('routes.frontdesk_discharge'))

@routes.route('/frontdesk/appointment_schedule')
@routes.route('/frontdesk/appointment_schedule/')
@login_required
@requires_access_level(3)
def frontdesk_appointment_schedule():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Patient_ID NOT IN (SELECT Patient_ID FROM Admitted)")
    patients = cur.fetchall()
    cur.close()
    print(patients)
    return render_template('frontdesk_appointment_schedule.html', patients=patients,  user = current_user)

@routes.route('/frontdesk/appointment_schedule/<patient_id>', methods=['GET', 'POST'])
@routes.route('/frontdesk/appointment_schedule/<patient_id>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(3)
def frontdesk_appointment_schedule_patient(patient_id):
    if request.method == 'POST':
        is_urgent = request.form.get('priority')
        if(is_urgent == 'Urgent'):
            date_to_schedule = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
            cur = mysql.connection.cursor()
            # start = '10:00:00'
            # end = '16:00:00'
            # for i in range(0, 6):
            #     start[1] = str(i)
            #     cur.execute("SELECT Doctor_ID")
            # min_time = '16:00:00'
            # cur.execute("SELECT Doctor_ID, MIN(Appointment_Time) FROM Appointment WHERE Appointment_Date = %s GROUP BY Doctor_ID", (date_to_schedule,))
            # min_time_doctor = cur.fetchall()
            # doctors_with_appointments = []
            # for doctor in min_time_doctor:
            #     doctors_with_appointments.append(doctor[0])
            # cur.execute("SELECT * FROM Doctor WHERE Doctor_ID NOT IN (%s)", (doctors_with_appointments,))
            # free_doctors = cur.fetchall()
            # if(len(free_doctors) != 0):
            #     doctor_id = free_doctors[0][0]
            #     cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doctor_id, date_to_schedule, '10:00:00'))
            # else:
            #     for 
            doctors_free = []
            cur.execute("SELECT Doctor_ID, Name FROM Doctor WHERE Doctor_ID NOT IN (SELECT Doctor_ID FROM Appointment WHERE Appointment_Date = %s)", (date_to_schedule,))
            doctors_free = cur.fetchall()
            if(len(doctors_free) != 0):
                doctors_id = doctors_free[0][0]
                cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doctors_id, date_to_schedule, '10:00:00'))
                mysql.connection.commit()
                flash(f'Appointment scheduled for patient {patient_id} at 10:00:00 with doctor {doctors_free[0][1]}', 'success')
                return redirect(url_for('routes.frontdesk_appointment_schedule'))
            
            else:
                start = '10:00:00'
                cur.execute("SELECT Doctor_ID, Name FROM Doctor")
                doctors = cur.fetchall()

                for i in range(0, 6):
                    start = start[0]+str(i)+start[2:]
                    for doc in doctors:
                        cur.execute("SELECT * FROM Appointment WHERE Doctor_ID = %s AND Appointment_Date = %s AND Appointment_Time = %s", (doc[0], date_to_schedule, start))
                        if(cur.fetchone() is None):
                            cur.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time) VALUES (%s, %s, %s, %s)", (patient_id, doc[0], date_to_schedule, start))
                            mysql.connection.commit()
                            flash(f'Appointment scheduled for patient {patient_id} at {start} with doctor {doc[1]}', 'success')
                            return redirect(url_for('routes.frontdesk_appointment_schedule'))
                        
                flash(f'No doctors available on urgent priority', 'danger')
                return redirect(url_for('routes.frontdesk_appointment_schedule'))
            
            # flash(f'Appointment scheduled for patient {patient_id}', 'success')
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Doctor")
            doctors = cur.fetchall()
            cur.close()
            return render_template('frontdesk_appointment_schedule_patient.html', patient_id=patient_id, doctors=doctors,  user = current_user)
    

@routes.route('/frontdesk/appointment_schedule/<patient_id>/<doctor_id>', methods=['GET', 'POST'])
@routes.route('/frontdesk/appointment_schedule/<patient_id>/<doctor_id>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(3)
def frontdesk_appointment_schedule_date(patient_id, doctor_id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        date_selected = request.form.get('date')
        cur_date = datetime.now().strftime("%Y-%m-%d")
        if date_selected <= cur_date:
            flash(f'Please select a date in the future', 'danger')
            return redirect(url_for('routes.frontdesk_appointment_schedule_patient', patient_id=patient_id))
            # return redirect(url_for('routes.frontdesk_appointment_schedule_date', patient_id=patient_id, doctor_id=doctor_id))
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
    
@routes.route('/admin', methods = ['GET', 'POST'])
@routes.route('/admin/', methods = ['GET', 'POST'])
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

@routes.route('/admin/edit_user', methods=['GET', 'POST'])
@routes.route('/admin/edit_user/', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_get_user():
    form = GetUser()
    if form.validate_on_submit():
        user_type = form.users.data
        return redirect(url_for('routes.admin_edit_user', user_type=user_type, user=current_user))
    return render_template('admin_select_user.html', form=form, user=current_user)

@routes.route('/admin/edit_user/<user_type>', methods=['GET', 'POST'])
@routes.route('/admin/edit_user/<user_type>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_edit_user(user_type):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT {user_type}_ID, Name, Address, Age, Gender, Personal_Contact FROM {user_type}")
    users = cur.fetchall()
    cur.close()

    form_1 = AddUser()
    if form_1.validate_on_submit():
        print("Form validated")
        cur = mysql.connection.cursor()
        # print(form_1.users.data, form_1.username.data)
        user = identify_class(user_type).get_by_username(form_1.username.data)
        if user:
            flash('Username already exists.', category='danger')
            return render_template('admin_add_del_user.html', user_type=user_type, user_type_list=users, form=form_1,  user=current_user)
        cur.execute(f"INSERT INTO {user_type} (Username, Password, Name, Address, Age, Gender, Personal_Contact) VALUES ('{form_1.username.data}', '{generate_password_hash(form_1.password1.data, method='sha256')}', '{form_1.name.data}', '{form_1.address.data}', '{form_1.age.data}', '{form_1.gender.data}', '{form_1.contact_number.data}')")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added user {form_1.name.data}', 'success')
        return redirect(url_for('routes.admin_edit_user', user_type=user_type, user=current_user))

    return render_template('admin_add_del_user.html', user_type=user_type, user_type_list=users, form=form_1,  user=current_user) 

@routes.route('/admin/delete/<user_type>/<user_id>', methods=['GET', 'POST'])
@routes.route('/admin/delete/<user_type>/<user_id>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_delete_user(user_type, user_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Treatment WHERE {user_type}_ID = {user_id}")
    mysql.connection.commit()
    cur.execute(f"DELETE FROM Appointment WHERE {user_type}_ID = {user_id}")
    mysql.connection.commit()
    cur.execute(f"DELETE FROM {user_type} WHERE {user_type}_ID = '{user_id}'")
    mysql.connection.commit()
    cur.close()
    flash(f'Successfully deleted {user_type} with ID {user_id}', 'success')
    return redirect(url_for('routes.admin_edit_user', user_type=user_type, user=current_user))

@routes.route('/admin/add_room', methods=['GET', 'POST'])
@routes.route('/admin/add_room/', methods=['GET', 'POST'])
@login_required
@requires_access_level(1)
def admin_add_room():
    form = AddRoom()
    if form.validate_on_submit():
        print("Form validated")
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO Room (Room_Num, Floor) VALUES ({form.num.data}, {form.floor.data})")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added room {form.num.data}', 'success')
        return redirect(url_for('routes.admin_add_room'))
    # else:
    #     flash(f'Error adding user {form.name.data}', 'danger')

    return render_template('admin_add_room.html', form=form,  user=current_user)

@routes.route('/dataentry')
@routes.route('/dataentry/')
@login_required
@requires_access_level(4)
def dataentry():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Test_ID , TestDate,  Category , Patient.Name, BodyPart FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0")
    incomplete_tests = cur.fetchall()
    cur.execute("SELECT Test_ID , TestDate,  Category , Patient.Name, BodyPart , Result FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 1")
    complete_tests = cur.fetchall()
    cur.execute("SELECT Treatment_ID, TreatmentDate, Category, Details, Doctor.Name, Patient.Name FROM Treatment JOIN Patient JOIN Doctor where Treatment.Patient_ID = Patient.Patient_ID and Treatment.Doctor_ID = Doctor.Doctor_ID")
    treatments = cur.fetchall()
    cur.close()
    print(incomplete_tests, complete_tests, treatments)
    return render_template('dataentry_main_dashboard.html', incomplete_tests=incomplete_tests, complete_tests=complete_tests, treatments=treatments, user=current_user)

@routes.route('/dataentry/test')
@routes.route('/dataentry/test/')
@login_required
@requires_access_level(4)
def dataentry_test():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Test_ID , TestDate,  Category , Name, BodyPart FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0")
    tests = cur.fetchall()
    cur.close()
    return render_template('dataentry_select_test.html', user=current_user,tests = tests)

@routes.route('/dataentry/test/<test_id>', methods=['GET', 'POST'])
@routes.route('/dataentry/test/<test_id>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(4)
def dataentry_test_id(test_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT TestDate,  Category , BodyPart , Name  FROM Test JOIN Patient where Test.Patient_ID = Patient.Patient_ID and Test.ResultObtained = 0 and Test.Test_ID = %s", (test_id,))
    test = cur.fetchone()
    cur.close()
    form = AddTestResult()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        if(form.file_upload.data is not None):
            filename = secure_filename(form.file_upload.data.filename)
            print(filename)
            print("HELLO")
            patient_data_path = os.getcwd() + '/test_patient_data/' + test_id + '/'
            if not os.path.exists(patient_data_path):
                os.makedirs(patient_data_path)
            form.file_upload.data.save(patient_data_path + filename)
            print(patient_data_path + filename)
            cur.execute(f"UPDATE Test SET ResultObtained = 1 , Result = '{form.result.data}', Document_Path = '{patient_data_path + filename}'WHERE Test_ID = '{test_id}'")
        else:
            cur.execute(f"UPDATE Test SET ResultObtained = 1 , Result = '{form.result.data}'WHERE Test_ID = '{test_id}'")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added test result {test[1]} for patient {test[3]}', 'success')
        return redirect(url_for('routes.dataentry'))
    return render_template('dataentry_add_test.html', user=current_user, test=test, form=form)

@routes.route('/dataentry/treatment')
@routes.route('/dataentry/treatment/')
@login_required
@requires_access_level(4)
def dataentry_select_patient():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Patient_ID,Name,Address,Age,Gender,Personal_Contact ,Emergency_Contact FROM Patient")
    patients = cur.fetchall()
    return render_template('dataentry_select_patient.html', user=current_user,patients = patients)

@routes.route('/dataentry/treatment/<patient_id>', methods=['GET', 'POST'])
@routes.route('/dataentry/treatment/<patient_id>/', methods=['GET', 'POST'])
@login_required
@requires_access_level(4)
def dataentry_select_doctor(patient_id):
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT Doctor_ID,Name,Username,Age,Gender,Personal_Contact FROM Doctor")
    doctors = cur.fetchall()
    cur.execute("SELECT Name FROM Patient WHERE Patient_ID = %s", (patient_id,))
    patient_name = cur.fetchone()
    form = AddTreatment()
    if form.validate_on_submit():
        if(form.file_upload.data is not None):
            filename = secure_filename(form.file_upload.data.filename)
            patient_data_path = os.getcwd() + '/treatment_patient_data/' + patient_id + '/'
            if not os.path.exists(patient_data_path):
                os.makedirs(patient_data_path)
            form.file_upload.data.save(patient_data_path + filename)
            cur.execute(f"INSERT INTO Treatment (Patient_ID, Doctor_ID, TreatmentDate, Category, Details, Document_Path) VALUES ('{patient_id}', '{form.doctor_id.data}', '{form.treatment_date.data}', '{form.category.data}', '{form.details.data}', '{patient_data_path + filename}')")
        else:
            cur.execute(f"INSERT INTO Treatment (Patient_ID, Doctor_ID, TreatmentDate, Category, Details) VALUES ('{patient_id}', '{form.doctor_id.data}', '{form.treatment_date.data}', '{form.category.data}', '{form.details.data}')")
        mysql.connection.commit()
        cur.close()
        flash(f'Successfully added treatment {form.category.data} for patient {form.patient.data} by doctor {form.doctor.data}', 'success')
        return redirect(url_for('routes.dataentry'))
    return render_template('dataentry_select_doctor.html', user=current_user,doctors = doctors, patient_name = patient_name, form = form)

# @routes.route('/dataentry/treatment/<patient_id>/<doctor_id>', methods=['GET', 'POST'])
# @routes.route('/dataentry/treatment/<patient_id>/<doctor_id>/', methods=['GET', 'POST'])
# @login_required
# @requires_access_level(4)
# def dataentry_treatment(patient_id, doctor_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT Name FROM Patient where Patient_ID = %s", (patient_id,))
#     patient = cur.fetchone()
#     cur.execute("SELECT Name FROM Doctor where Doctor_ID = %s", (doctor_id,))
#     doctor = cur.fetchone()
#     patient = patient[0]
#     doctor = doctor[0]
#     print(patient)
#     print(doctor)
#     cur.close()
#     form = AddTreatment()
#     if form.validate_on_submit():
#         print("Form validated")
#         cur = mysql.connection.cursor()
#         if(form.file_upload.data is not None):
#             filename = secure_filename(form.file_upload.data.filename)
#             patient_data_path = os.getcwd() + '/patient_data/' + patient_id + '/'
#             if not os.path.exists(patient_data_path):
#                 os.makedirs(patient_data_path)
#             form.file_upload.data.save(patient_data_path + filename)
#             cur.execute(f"INSERT INTO Treatment (Patient_ID, Doctor_ID, TreatmentDate, Category, Details, Document_Path) VALUES ('{patient_id}', '{doctor_id}', '{form.treatment_date.data}', '{form.category.data}', '{form.details.data}', '{patient_data_path + filename}')")
#         else:
#             cur.execute(f"INSERT INTO Treatment (Patient_ID, Doctor_ID, TreatmentDate, Category, Details) VALUES ('{patient_id}', '{doctor_id}', '{form.treatment_date.data}', '{form.category.data}', '{form.details.data}')")
#         mysql.connection.commit()
#         cur.close()
#         flash(f'Successfully added treatment {form.category.data} for patient {patient} by doctor {doctor}', 'success')
#         return redirect(url_for('routes.dataentry'))
#     return render_template('dataentry_add_treatment.html', user=current_user, patient=patient, doctor=doctor, form=form)

# @routes.route("/send/<patient_id>/<doctor_id>/<file>", methods = ["GET"])
# def index(patient_id,doctor_id,file):
#     extension = file[-3:]
#     file = f"./HMS/public/{file}"
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT Username,Name FROM Doctor WHERE Doctor_ID = %s", (doctor_id,))
#     doctor = cur.fetchone()
#     cur.execute("SELECT Name,Age,Gender FROM Patient WHERE Patient_ID = %s", (patient_id,))
#     patient = cur.fetchone()
#     cur.close()
#     subject = f"Health Report for {patient[0]}"
#     body = f"Dear {doctor[1]},\n\nPlease find the attached health report for {patient[0]}.\n\nRegards,\nHMS Team"
#     msg = Message(subject = subject, body = body, sender = app.config['MAIL_USERNAME'], recipients = ['kushaz.sehgal@gmail.com'])
#     if extension == 'pdf':
#         content_type = 'application/pdf'
#     elif extension == 'png':
#         content_type = 'image/png'    
#     elif extension == 'txt':
#         content_type = 'text/plain'
#     with app.open_resource(file) as fp:  
#         msg.attach(f"{patient[0]}_report.{extension}",content_type,fp.read())  
#         # msg.attach(f"{patient[0]}_report2.{extension}",content_type,fp.read()) 
#     with app.open_resource('./public/A2.pdf') as fp:  
#         msg.attach(f"{patient[0]}_report2.pdf",'application/pdf',fp.read())          
#     mail.send(msg)  
#     return "sent"  

