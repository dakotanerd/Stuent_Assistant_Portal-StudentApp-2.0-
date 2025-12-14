import os
import pytest
from flask import url_for 
from app import create_app, db
from app.main.models import User, Student, Teacher, Course, CourseSection, CourseApplication, PastEnrollments, AcceptedStudent
from config import Config
import sqlalchemy as sqla

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.test_request_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_user(username, email, firstname, lastname, address, passwd):
    user = Student(username = username, email = email, firstname = firstname, lastname = lastname, address = address)
    user.set_password(passwd)
    return user

#only need to add courses to db, all other db info will be added through routes
@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    # initialize the courses
    #major, coursenum, title, year
    if Course.query.count() == 0:
        courses = [{'major':'CS','coursenum':'3733', 'title':'soft eng', 'year':'2025'},{'major':'CS','coursenum':'1000', 'title':'intro to cs', 'year':'2025'},
                   {'major':'EE','coursenum':'1000', 'title':'wiring', 'year':'2025'},{'major':'ME','coursenum':'1000', 'title':'intro to mech eng', 'year':'2025'},
                   {'major':'MATH','coursenum': '1000', 'title':'calc 1', 'year':'2025'}  ]
        for t in courses:
            db.session.add(Course(major=t['major'],coursenum=t['coursenum'], title=t['title'], year=t['year']))
        db.session.commit()

<<<<<<< HEAD
    s = Student('ethan', 'ethan', 'carter', 123456789, 'ecarter@wpi.edu', 1234567890, 'Computer Science', '3.5', 2026)
    s.set_password('1')
    db.session.add(s)

    t = Teacher('dakota', 'dakota', 'wellerbrady', 198765432, 'dakota@wpi.edu', 1098765432, 'Computer Science')
    t.set_password('1')
    db.session.add(t)

=======
    s = Student(username='ethan', firstname='ethan', lastname='carter', wpi_id=123456789, email='ecarter@wpi.edu', phone=1234567890, major='Computer Science', gpa='3.5', graduation_year=2026)
    s.set_password('1')
    db.session.add(s)

    t = Teacher(username='dakota', firstname='dakota', lastname='wellerbrady', wpi_id=198765432, email='dakota@wpi.edu', phone=1098765432, department='Computer Science')
    t.set_password('1')
    db.session.add(t)

    teacher = db.session.scalars(sqla.select(Teacher).where(Teacher.username == 'dakota')).first()
    course = db.session.scalars(sqla.select(Course).where(Course.title == 'soft eng')).first()
    section = CourseSection(term='a', year='2025', teacher_id=teacher.id, course_id=course.id, num_sa=3, min_gpa='2', min_grade='a')
    db.session.add(section)

    student = db.session.scalars(sqla.select(Student).where(Student.username == 'ethan')).first()
    section = db.session.scalars(sqla.select(CourseSection).where(CourseSection.teacher_id == teacher.id and CourseSection.course_id == course.id)).first()
    application = CourseApplication(student_id=student.id, course_id=course.id, section_id=section.id, reason='I want money')
    db.session.add(application)

>>>>>>> b3b6c4e1eadf56eb7872e0713309af18bb663aeb
    db.session.commit()     # Commit the changes 

    yield  # this is where the testing happens!

    db.drop_all()

#auth route tests

def test_login_page(request, test_client):
    response = test_client.get('/user/login')
    assert response.status_code == 200
    assert b"Click to Register as a Student!" in response.data

def test_student_register_page(request, test_client):
    response = test_client.get('/student/register')
    assert response.status_code == 200
    assert b"Student Registration" in response.data

def test_student_register(request,test_client, init_database):
    response = test_client.post('/student/register',
                                data=dict(username='test', firstname='te', lastname='st', email='test@wpi.edu', wpi_id='111111111', phone='1111111111',
                                          major='Computer Science', gpa=3.5, grad_year='2026', password='1', password2='1'),
                                          follow_redirects=True)
    
    assert response.status_code == 200
    s = db.session.scalars(sqla.select(Student).where(Student.username == 'test')).first()
    s_count = db.session.scalars(sqla.select(Student).where(Student.username == 'test')).all()

    assert s.lastname == 'st'
    assert len(s_count) == 1
    #application should redirect to login page
    assert b"Congratulations, you have been registered as a student!" in response.data
    assert b"Please log in to access this page." in response.data
    assert b"Sign In" in response.data

def test_teacher_register_page(request, test_client):
    response = test_client.get('/teacher/register')
    assert response.status_code == 200
    assert b"Teacher Registration" in response.data

def test_teacher_register(request, test_client, init_database):
    response = test_client.post('/teacher/register',
                                data=dict(username='teacher', firstname='teach', lastname='er', email='teacher@wpi.edu', wpi_id='122222222', phone='1222222222',
                                          department='Computer Science',password='1', password2='1'),
                                          follow_redirects=True)
    assert response.status_code == 200
    assert b"Congratulations, you have been registered as a teacher!" in response.data
    assert b"Please log in to access this page." in response.data
    assert b"Sign In" in response.data

def test_invalidlogin(request, test_client, init_database):
    response = test_client.post('/user/login',
<<<<<<< HEAD
                                data=dict(username='ethan', password='12345', remember_me=False))
=======
                                data=dict(username='ethan', password='12345', remember_me=False),
                                follow_redirects=True)
>>>>>>> b3b6c4e1eadf56eb7872e0713309af18bb663aeb
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"Sign In" in response.data

#helper functions
<<<<<<< HEAD
def login(test_client, path, username, password):
=======
def login(test_client, init_database, path, username, password):
>>>>>>> b3b6c4e1eadf56eb7872e0713309af18bb663aeb
    response = test_client.post(path,
                                data=dict(username=username, password=password, remember_me=False),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"has successfully logged in!" in response.data

def logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200
    # Assuming the application re-directs to login page after logout. 
    assert b"Sign In" in response.data

def test_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
<<<<<<< HEAD
    login(test_client, path = '/user/login', username = 'ethan', password = '1')
=======
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
>>>>>>> b3b6c4e1eadf56eb7872e0713309af18bb663aeb

    logout(test_client, path = '/student/logout')

#student routes tests
<<<<<<< HEAD
#index
=======
#index - get
def test_student_index(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    response = test_client.get('/student/index')
    assert response.status_code == 200
    assert b"Recommended Courses" in response.data
    logout(test_client, path = '/student/logout')
#application - get post
def test_student_application(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    section = db.session.scalars(sqla.select(CourseSection)).first()
    response = test_client.get('/student/application/{}'.format(section.id))
    assert response.status_code == 200
    assert b"Apply for" in response.data
    logout(test_client, path = '/student/logout')
#display_Student_profile - get
def test_student_profile_display(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    response = test_client.get('/student/profile')
    assert response.status_code == 200
    assert b"View Profile" in response.data
    logout(test_client, path = '/student/logout')
#add_course - get post
def test_student_enrollment(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    response = test_client.get('/student/course/add')
    assert response.status_code == 200
    assert b"Add past enrollment" in response.data
    logout(test_client, path = '/student/logout')
#edit_student_profile - get post
def test_student_profile_edit(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    response = test_client.get('/student/edit/profile')
    assert response.status_code == 200
    assert b"Edit Your Profile" in response.data
    logout(test_client, path = '/student/logout')
#edit_application - get post
def test_edit_app(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'ethan', password = '1')
    response = test_client.get('/student/edit/application/1')
    assert response.status_code == 200
    assert b"Edit Application" in response.data
    logout(test_client, path = '/student/logout')
#delete_application - post
#delete_past_enrollment - post


#teacher route tests
#index - get
def test_teacher_index(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'dakota', password = '1')
    response = test_client.get('/teacher/index')
    assert response.status_code == 200
    assert b"My Sections" in response.data
    logout(test_client, path = '/student/logout')
#create_section - get post
def test_teacher_create(request, test_client, init_database):
    login(test_client, init_database, path = '/user/login', username = 'dakota', password = '1')
    response = test_client.get('/course/section/create')
    assert response.status_code == 200
    assert b"Create A Course Section" in response.data
    logout(test_client, path = '/student/logout')
#display_Teacher_profile - get
#update_application_status - post
#view_section_applications - get
#view_profile
#teacher_edit_course - get post
#teacher_delete_section - post
>>>>>>> b3b6c4e1eadf56eb7872e0713309af18bb663aeb
