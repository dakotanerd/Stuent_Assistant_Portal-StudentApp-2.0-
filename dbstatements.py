from app import db
from app.main.models import User, Student, Teacher, Course, CourseSection
from config  import Config

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import os

#student
#username, firstname, lastname, wpi_id, email, phone, major, GPA, graduation_year

s = Student(username = "ecarter", firstname = "Ethan", lastname = "Carter", wpi_id = 111111111, email = "ecarter@wpi.edu", phone = 1111111111, major = "CS", GPA = "3.93", graduation_year = 2026, user_type = "Student")
db.session.add(s)
db.session.commit()

result = db.session.scalars(sqla.select(User)).first()
print(result)

import sqlalchemy as sqla
db.session.scalars(sqla.select(Course)).all()
import sqlalchemy as sqla
db.session.scalars(sqla.select(CourseSection)).all()