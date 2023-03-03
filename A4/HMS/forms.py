from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange

class RegisterPatient(FlaskForm):
    name = StringField("Patient Name", validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField("Patient Address", validators=[DataRequired(), Length(min=2, max=50)])
    age = IntegerField("Patient Age", validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = StringField("Patient Gender", validators=[DataRequired(), Length(min=4, max=10)])
    contact_number = StringField("Patient Contact Number", validators=[DataRequired(), Length(min=10, max=10)])
    emergency_contact = StringField("Patient Emergency Contact", validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField("Register Patient")

class AddUser(FlaskForm):
    choices = [('Doctor', 'Doctor'), ('FD_Operator', 'FrontDesk Operator'), ('DE_Operator', 'DataEntry Operator')]
    users = SelectField(u'Field name', choices = choices, validators = [DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=50)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=20)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password1')])
    name = StringField("User's Name", validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField("User's Address", validators=[DataRequired(), Length(min=2, max=50)])
    age = IntegerField("User's Age", validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = StringField("User's Gender", validators=[DataRequired(), Length(min=4, max=10)])
    contact_number = StringField("User's Contact Number", validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField("Add User")

class DeleteUser(FlaskForm):
    choices = [('Doctor', 'Doctor'), ('FD_Operator', 'FrontDesk Operator'), ('DE_Operator', 'DataEntry Operator')]
    users = SelectField(u'Field name', choices = choices, validators = [DataRequired()])
    submit = SubmitField("Select User")
