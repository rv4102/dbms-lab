from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange

class RegisterPatient(FlaskForm):
    name = StringField("Patient Name", validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField("Patient Address", validators=[DataRequired(), Length(min=2, max=50)])
    age = IntegerField("Patient Age", validators=[DataRequired(), NumberRange(min=1, max=120)])
    gender = StringField("Patient Gender", validators=[DataRequired(), Length(min=4, max=10)])
    contact_number = StringField("Patient Contact Number", validators=[DataRequired(), Length(min=10, max=10)])
    emergency_contact = StringField("Patient Emergency Contact", validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField("Register Patient")


