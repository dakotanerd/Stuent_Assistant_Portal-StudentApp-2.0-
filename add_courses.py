from config import Config
from app import create_app, db
from app.main.models import User, Student, Teacher, Course, CourseSection
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'user': User, 'Student': Student, 'Teacher': Teacher , 'Course': Course, 'CourseSection': CourseSection}


app.app_context().push()

def add_courses():
    existing_courses = db.session.query(Course).all()
    if not existing_courses:  # Only add courses if the table is empty
        courses = [
            {'major': 'CS', 'coursenum': '3733', 'title': 'soft eng', 'year': '2000'},
            {'major': 'CS', 'coursenum': '2000', 'title': 'object oriented', 'year': '2000'},
            {'major': 'CN', 'coursenum': '1000', 'title': 'Nihao', 'year': '2000'},
            {'major': 'DS', 'coursenum': '1500', 'title': 'graphs and data and stuff', 'year': '2000'}
        ]
        for c in courses:
            db.session.add(Course(major=c['major'], coursenum=c['coursenum'], title=c['title'], year=c['year']))
        db.session.commit()

add_courses()
existing_courses = db.session.query(Course).all()
print(existing_courses)