from flask_wtf import Form
from wtforms import StringField, PasswordField, DateTimeField, IntegerField, RadioField, TextAreaField, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo, number_range)

from models import User


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')



class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class ApplyForm(Form):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = StringField('Date of Birth', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    graduation = StringField('Expected Graduation', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    github = StringField('Github username optional')
    paragraph = TextAreaField(validators=[Length(max=150)])
    accept_tos = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()])