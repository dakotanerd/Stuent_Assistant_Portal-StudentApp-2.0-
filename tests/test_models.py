import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.main.models import User, Teacher, Student, Course, PastEnrollments, CourseSection, CourseApplication, AcceptedStudent
from app.main.models import Course, Student, User, Teacher, CourseSection, CourseApplication
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class TestModels(unittest.TestCase):
    #tests app setup
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_hashing(self):
        user = Student(username = 'user', 
                       firstname = 'user', 
                       lastname = 'name', 
                       wpi_id = '123456789', 
                       email = 'user@wpi.edu', 
                       phone = '1234567890')
        user.set_password('notuser')
        self.assertFalse(user.check_password('user'))
        self.assertTrue(user.check_password('notuser'))

    ######## ADD TEST USERTYPE (teacher or student?) ########
    ######## ADD TEST MAKE COURSE ########
    ######## ADD TEST PAST ENROLLMENTS ########
    ######## ADD TEST COURSE ENROLLMENTS ########

    def test_user_creation(self):
        """Test creating a regular user."""
        user = User(username='testuser', firstname='Test', lastname='User', wpi_id=123456789,
                    email='testuser@wpi.edu', phone=1234567890)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertTrue(retrieved_user.check_password('password'))

    def test_teacher_creation(self):
        """Test creating a teacher usertype."""
        teacher = Teacher(username='teacher', firstname='Teach', lastname='Math', wpi_id=987654321,
                          email='teach@wpi.edu', phone=9876543210, department='Mathematics')
        teacher.set_password('securepassword')
        db.session.add(teacher)
        db.session.commit()

        retrieved_teacher = Teacher.query.first()
        self.assertIsNotNone(retrieved_teacher)
        self.assertEqual(retrieved_teacher.department, 'Mathematics')

    def test_student_creation(self):
        """Test creating student usertype."""
        student = Student(username='student', firstname='Student', lastname='Horrible', wpi_id=111111111,
                          email='student@wpi.edu', phone=5555555555, major='Computer Science', gpa='3.8',
                          graduation_year=2025)
        student.set_password('studentpassword')
        db.session.add(student)
        db.session.commit()

        retrieved_student = Student.query.first()
        self.assertIsNotNone(retrieved_student)
        self.assertEqual(retrieved_student.major, 'Computer Science')

    def test_course_creation(self):
        """Test creating course."""
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(course)
        db.session.commit()

        retrieved_course = Course.query.first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.title, 'Intro to Programming')

    def test_course_section_creation(self):
        """Test creating course section."""
        teacher = Teacher(username='teachercs', firstname='Teach', lastname='CS', wpi_id=987654322,
                          email='teachcs@wpi.edu', phone=9876543210, department='Computer Science')
        teacher.set_password('securepassword')
        db.session.add(teacher)
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(course)
        db.session.commit()

        section = CourseSection(term='A', year='2024', teacher_id=teacher.id, course_id=course.id,
                                 num_sa=2, min_gpa=3.0, min_grade='B')
        db.session.add(section)
        db.session.commit()

        retrieved_section = CourseSection.query.first()
        self.assertIsNotNone(retrieved_section)
        self.assertEqual(retrieved_section.term, 'A')

    def test_course_application(self):
        """Test creating a course application."""
        student = Student(username='student2', firstname='Student2', lastname='Horrible', wpi_id=111111112,
                          email='student2@wpi.edu', phone=6666666666, major='Computer Science', gpa='3.8',
                          graduation_year=2025)
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(student)
        db.session.add(course)
        db.session.commit()

        application = CourseApplication(student_id=student.id, course_id=course.id, reason='Get me outta here')
        db.session.add(application)
        db.session.commit()

        retrieved_application = CourseApplication.query.first()
        self.assertIsNotNone(retrieved_application)
        self.assertEqual(retrieved_application.reason, 'Get me outta here')

    ######## ADD TEST USERTYPE (teacher or student?) ########
    ######## ADD TEST MAKE COURSE ########
    ######## ADD TEST PAST ENROLLMENTS ########
    ######## ADD TEST COURSE ENROLLMENTS ########

    def test_user_creation(self):
        """Test creating a regular user."""
        user = User(username='testuser', firstname='Test', lastname='User', wpi_id=123456789,
                    email='testuser@wpi.edu', phone=1234567890)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertTrue(retrieved_user.check_password('password'))

    def test_teacher_creation(self):
        """Test creating a teacher usertype."""
        teacher = Teacher(username='teacher', firstname='Teach', lastname='Math', wpi_id=987654321,
                          email='teach@wpi.edu', phone=9876543210, department='Mathematics')
        teacher.set_password('securepassword')
        db.session.add(teacher)
        db.session.commit()

        retrieved_teacher = Teacher.query.first()
        self.assertIsNotNone(retrieved_teacher)
        self.assertEqual(retrieved_teacher.department, 'Mathematics')

    def test_student_creation(self):
        """Test creating student usertype."""
        student = Student(username='student', firstname='Student', lastname='Horrible', wpi_id=111111111,
                          email='student@wpi.edu', phone=5555555555, major='Computer Science', gpa='3.8',
                          graduation_year=2025)
        student.set_password('studentpassword')
        db.session.add(student)
        db.session.commit()

        retrieved_student = Student.query.first()
        self.assertIsNotNone(retrieved_student)
        self.assertEqual(retrieved_student.major, 'Computer Science')

    def test_course_creation(self):
        """Test creating course."""
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(course)
        db.session.commit()

        retrieved_course = Course.query.first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.title, 'Intro to Programming')

    def test_course_section_creation(self):
        """Test creating course section."""
        teacher = Teacher(username='teachercs', firstname='Teach', lastname='CS', wpi_id=987654322,
                          email='teachcs@wpi.edu', phone=9876543210, department='Computer Science')
        teacher.set_password('securepassword')
        db.session.add(teacher)
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(course)
        db.session.commit()

        section = CourseSection(term='A', year='2024', teacher_id=teacher.id, course_id=course.id,
                                 num_sa=2, min_gpa=3.0, min_grade='B')
        db.session.add(section)
        db.session.commit()

        retrieved_section = CourseSection.query.first()
        self.assertIsNotNone(retrieved_section)
        self.assertEqual(retrieved_section.term, 'A')

    def test_course_application(self):
        """Test creating a course application."""
        student = Student(username='student2', firstname='Student2', lastname='Horrible', wpi_id=111111112,
                          email='student2@wpi.edu', phone=6666666666, major='Computer Science', gpa='3.8',
                          graduation_year=2025)
        course = Course(major='CS', coursenum='1010', title='Intro to Programming', year='2024')
        db.session.add(student)
        db.session.add(course)
        db.session.commit()

        application = CourseApplication(student_id=student.id, course_id=course.id, reason='Get me outta here')
        db.session.add(application)
        db.session.commit()

        retrieved_application = CourseApplication.query.first()
        self.assertIsNotNone(retrieved_application)
        self.assertEqual(retrieved_application.reason, 'Get me outta here')

if __name__ == '__main__':
    unittest.main(verbosity=2)