from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, Email, NumberRange, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
import sqlalchemy as sqla
from app import db
from app.main.models import Course



def GPA_length_check(form, field):
    # Convert the GPA to a string and remove the decimal point for length validation
    gpa_str = str(field.data)
    if len(gpa_str.replace('.', '')) > 4:
        raise ValidationError("GPA cannot exceed 4 digits in total.")

class SectionForm(FlaskForm):
    # section fields
    course = QuerySelectField('Course',
                              query_factory=lambda: db.session.scalars(sqla.select(Course)),
                              get_label=lambda course: course.title,
                              allow_blank=False)
    term = SelectField('Term',
                       choices=[('a', 'A'),
                                ('b', 'B'),
                                ('c', 'C'),
                                ('d', 'D')])
    year = StringField('Course Year', validators=[
        DataRequired(),
        Length(min=4, max=4, message="Year must be exactly 4 digits."),
        Regexp(r'^\d{4}$', message="Year must be a 4-digit number.")
    ])
    section_num = StringField('Course Section Number', validators=[DataRequired(), Length(min=2, max=2)])

    # sa-ship fields
    sa_num = StringField('Number of SA\'s', validators=[DataRequired(), Length(max=1)])
    min_gpa = FloatField('GPA', validators=[
        DataRequired(),
        NumberRange(min=0.0, max=4, message="GPA must be between 0.0 and 4.0"),
        GPA_length_check  # Apply custom GPA length check
    ])
    min_grade = SelectField('Minimum Required Grade',
                            choices=[('a', 'A'),
                                     ('b', 'B'),
                                     ('c', 'C')])
    
    submit = SubmitField('Create!')

class StudentCourseForm(FlaskForm):
    course = QuerySelectField('Course',
                              query_factory=lambda: db.session.scalars(sqla.select(Course)),
                              get_label=lambda course: course.title,
                              allow_blank=False)
    term = SelectField('Term',
                       choices=[('a', 'A'),
                                ('b', 'B'),
                                ('c', 'C'),
                                ('d', 'D')])
    year = StringField('Course Year', validators=[
        DataRequired(),
        Length(min=4, max=4, message="Year must be exactly 4 digits."),
        Regexp(r'^\d{4}$', message="Year must be a 4-digit number.")
    ])
    section_num = StringField('Course Section Number', validators=[DataRequired(), Length(min=2, max=2)])
    grade = SelectField('Grade Received',
                        choices=[('a', 'A'),
                                 ('b', 'B'),
                                 ('c', 'C'),
                                 ('nr', 'NR')])
    
    # Added sa_before field
    sa_before = BooleanField('Have you been an SA for this course before?', default=False)
    
    submit = SubmitField('Submit')


class EditStudentProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=40)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=40)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])

    # WPI ID field
    wpi_id = StringField('WPI ID', validators=[
        DataRequired(),
        Length(min=10, max=10, message="Please enter a valid ID number (10 digits)."),
        Regexp(r'^\d{10}$', message="ID must be exactly 10 digits, without spaces or dashes.")
    ])

    # Updated phone field to StringField to handle phone formats
    phone = StringField('Phone', validators=[
        DataRequired(),
        Length(min=10, max=10, message="Please enter a valid phone number (10 digits)."),
        Regexp(r'^\d{10}$', message="Phone number must be exactly 10 digits, without spaces or dashes.")
    ])

    # GPA validation
    gpa = FloatField('GPA', validators=[
        DataRequired(),
        NumberRange(min=0.0, max=4, message="GPA must be between 0.0 and 4.0"),
        GPA_length_check  # Apply custom GPA length check
    ])

    major = StringField('Major', validators=[Optional()])
    submit = SubmitField('Save Changes')