from flask_wtf import Form
from wtforms import StringField, PasswordField, DateTimeField, IntegerField, RadioField, TextAreaField, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo, number_range)

from models import User, Apply, emailSignup


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
    emailapp = StringField('Email', validators=[DataRequired(), Email()])
    birthday = StringField('Date of Birth', validators=[DataRequired()])
    phone = IntegerField('Phone Number', validators = [DataRequired()])
    graduation = StringField('Expected Graduation', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    github = StringField('Github username optional')
    #paragraph = TextAreaField(validators=[Length(max=150)])

class Rsvp(Form):
    attend = RadioField('Can you attend?', choices=[('Yes', 'Yes I will be there'), ('No', 'No, I can not make it')])
    how = RadioField('How did you hear about us?', choices=[('MLH Website','MLH Website'),('School Presentation','School Presentation'),('Social Media','Social Media'), ('School Mailing List','School Mailing List'), ('Other Hackathon','Other Hackathon'), ('Banner Advertisement'), ('Others', 'Others')])
    shirtSize = RadioField('What is your shirt size?', choices=[('Extra Small', 'XSmall'), ('Small', 'Small'), ('Medium', 'Medium' ), ('Large','Large'), ('XLarge'), ('XXLarge (Grizzly Size)')] )


class signup(Form):
    emailaddress = StringField('Email', validators=[DataRequired(), Email()])