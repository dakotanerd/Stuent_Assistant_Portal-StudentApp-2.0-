from typing import Optional
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError, NumberRange, Optional
from wtforms_sqlalchemy.fields import QuerySelectField , QuerySelectMultipleField

import sqlalchemy as sqla
from app import db
from app.main.models import Student, Teacher, User


class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=9)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    major = SelectField('Major',
                             choices= [('Computer Science', 'Computer Science'), #can add more in later iterations
                                       ('Mathematics', 'Mathematics'),
                                       ('Robotics', 'Robotics'),
                                       ('Psychology', 'Psychology'),
                                       ('Data Science', 'Data Science'),
                                       ('IMGD','IMGD'),
                                       ('Biology', 'Biology'),
                                       ('Chemistry', 'Chemistry'),
                                       ('Social Science and Policy Studies', 'Social Science and Policy Studies'),
                                       ('Environmental Engineering', 'Mechanical Engineering'),
                                       ('Environmental Engineering','Environmental Engineering'),
                                       ('Spanish', 'Spanish'),
                                       ('Mandarin','Mandarin' )]
                                       )
    gpa = FloatField('Overall GPA', validators=[
        Optional(),
        NumberRange(min=0.0, max=4.0, message="GPA must be between 0.0 and 4.0")
    ])
    grad_year = StringField('Year of Graduation',validators=[DataRequired(), Length(min=4, max=4)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')    

    def validate_username(self, username):
        query = sqla.select(Student).where(Student.username == username.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('This username already exists! Please use a different username')

    def validate_email(self, email):
        query = sqla.select(Student).where(Student.email == email.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('This email already exists! Please use a different email')

class TeacherRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9,max=9)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])    
    department = SelectField('Department',
                             choices= [('Computer Science', 'Computer Science'), #can add more in later iterations
                                       ('Mathematics', 'Mathematics'),
                                       ('Robotics', 'Robotics'),
                                       ('Psychology', 'Psychology'),
                                       ('Data Science', 'Data Science'),
                                       ('IMGD','IMGD'),
                                       ('Biology', 'Biology'),
                                       ('Chemistry', 'Chemistry'),
                                       ('Social Science and Policy Studies', 'Social Science and Policy Studies'),
                                       ('Environmental Engineering', 'Mechanical Engineering'),
                                       ('Environmental Engineering','Environmental Engineering'),
                                       ('Spanish', 'Spanish'),
                                       ('Mandarin','Mandarin' )]
                                       )
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')    

    def validate_username(self, username):
        query = sqla.select(Teacher).where(Teacher.username == username.data)
        teacher = db.session.scalars(query).first()
        if teacher is not None:
            raise ValidationError('This username already exists! Please use a different username')

    def validate_email(self, email):
        query = sqla.select(Teacher).where(Teacher.email == email.data)
        teacher = db.session.scalars(query).first()
        if teacher is not None:
            raise ValidationError('This email already exists! Please use a different email')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')