from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, FileField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class UploadQuestionPaperForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired()])
    month = StringField('Month', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    pdf_file = FileField('Upload PDF', validators=[DataRequired()])
    submit = SubmitField('Upload')