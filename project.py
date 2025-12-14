from config import Config
from app import create_app, db
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.models import User, Student, Teacher, Course, CourseSection
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
import identity.web

app = create_app(Config)

app.jinja_env.globals.update(Auth=identity.web.Auth)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'user': User, 'Student': Student, 'Teacher': Teacher , 'Course': Course, 'CourseSection': CourseSection}

@sqla.event.listens_for(Course.__table__, 'after_create')
def add_courses(*args, **kwargs):
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


@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        add_courses()

if __name__ == "__main__":
    app.run(debug=True)