# Hospital Management System

## What is it?

This is a web application written in **Python Flask** and **Bootstrap CSS** with the following features :
1. Implements Access Control through the use of Python decorators (**Flask-Login**).
2. Supports automated weekly email reports to Doctor about Patient health using **Flask-APScheduler**.
3. Generate PDF reports from webpage using **PDFKit**.
4. Secure storage of passwords in MySQL database using **Werkzeug** password hashing.

## Dependencies

1. [mysql](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
2. python@3.10
3. All packages in requirements.txt (`python3 -m pip install -r requirements.txt`)
4. wkhtmltopdf (`sudo apt install wkhtmltopdf`)

## Instructions

1. Create a file '.env' in the 'src' folder and add the following two lines in it:
```
MYSQL_USER='username'
MYSQL_PASSWORD='password'
```
Where the credentials will be the ones you use to login to mysql server.

2. `python3 run.py`
3. To add users to database, navigate to http://localhost:5000/sign-up and add the users needed. Navigate back to login page (http://localhost:5000) and sign in as that user.
4. To Reinitialize Database => mysql -u root -p < src/hospital_db.sql

## Screenshots

1. [Relational Schema for Hospital Management System](/images/schema.png)
2. [Admin Dashboard](/images/admin_dashboard.png)
3. [Admin Add/Delete User](/images/admin_add_del.png)
4. [Login Page](/images/login.png)
5. [Pop-Up in case of unauthorised access](/images/login_unauthorised.png)
6. [Frontdesk Operator's Dashboard](/images/fdo_dashboard.png)
7. [Register Patient Page](/images/fdo_register.png)
8. [Admit Patient Page](/images/fdo_admit.png)
9. [Schedule an Appointment Page](/images/fdo_appt.png)
10. [Schedule a 'Normal' Appointment Page (date selector)](/images/fdo_appt_date.png)
11. [DataEntry Operator's Dashboard](/images/deo_dashboard.png)
12. [DataEntry Operator Add Treatment](/images/deo_add_treatment.png)
13. [DataEntry Operator Treatment Form](/images/deo_treatment_filled.png)
14. [DataEntry Operator Add Test Result](/images/deo_add_test.png)
15. [DataEntry Operator Test Form](/images/deo_test_filled.png)
16. [Doctor Dashboard](/images/doc_dashboard.png)
17. [Doctor Query Patients](/images/doc_query_patients.png)
18. [Doctor Add Test](/images/doc_add_test.png)