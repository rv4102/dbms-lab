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

