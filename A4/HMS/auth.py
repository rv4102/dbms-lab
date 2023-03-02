from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import session
from flask_mysqldb import MySQL
from .models import Administrator, Doctor, FD_Operator, DE_Operator, identify_class

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        staff = identify_class(request.form.get('role'))
        username = request.form.get('username')
        password = request.form.get('password')
        user_IDs = staff.get_by_username(username)
        user = user_IDs[0]
        # iterate through user and match password until possible login
        print(user_IDs)
        print(user.Password)
        print(password)
        print(check_password_hash(user.Password, password))
        if user and check_password_hash(user.Password, password):
            print("Insecure")
            session['Access_Level'] = user.AccessLevel
            login_user(user, remember=True)
            flash('Logged in successfully.', category='success')
            return redirect(url_for('routes.index'))
        flash('Incorrect username or password.', category='error')
    return render_template('login.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        staff_type = identify_class(request.form.get('role'))
        
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        District = request.form.get('District')
        PIN = request.form.get('PIN')
        House = request.form.get('House')
        Age = request.form.get('Age')
        Gender = request.form.get('Gender')
        Personal_Contact = request.form.get('Personal_Contact')
        for staff in [Administrator, Doctor, FD_Operator, DE_Operator]:
            user = staff.get_by_username(email)
            if user:
                flash('Email already exists.', category='error')
                return render_template("sign_up.html", user = current_user)
        
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            temp = len(staff_type.get_all())
            new_user = staff_type.create(temp+1,email, first_name, generate_password_hash(password1, method='sha256'), District, PIN, House, Age, Gender, Personal_Contact)
            print(new_user)
            session['Access_Level'] = new_user.AccessLevel
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('routes.index'))
        
    return render_template("sign_up.html", user=current_user)
