from flask_wtf import Form
from wtforms import BooleanField, StringField, validators, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
#from app.models import Account


class SignUpForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(max=30), validators.length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    tandc = BooleanField('TandC', validators=[DataRequired()])

class LogInForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(max=30), validators.length(min=8)])
    remember = BooleanField('Stay Signed In')

class CreateGroupForm(Form):
    groupName = StringField('Group Name', validators=[DataRequired(), validators.length(max=30), validators.length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(max=30), validators.length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class JoinGroupForm(Form):
    groupName = StringField('Group Name', validators=[DataRequired(), validators.length(max=30), validators.length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), validators.length(max=30), validators.length(min=8)])

class EntryForm(Form):
    entry = TextAreaField('Entry', validators=[DataRequired(), validators.length(max=400), validators.length(min=2)])
    loc = StringField('Location', validators=[DataRequired(), validators.length(max=50), validators.length(min=2)])
    grpName = StringField('Group Name', validators=[DataRequired(), validators.length(max=30), validators.length(min=3)])
    grpPswrd = PasswordField('Password', validators=[DataRequired(), validators.length(max=30), validators.length(min=8)])
