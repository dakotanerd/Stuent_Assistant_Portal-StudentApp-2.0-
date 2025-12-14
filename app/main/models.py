from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash   
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from sqlalchemy import exc

from app import login
from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    # traits
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(40))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(40))
    wpi_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120))
    phone : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10))

    password_hash : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))


    # auto-mapping for user type
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
        'polymorphic_identity' : 'User',
        'polymorphic_on' : user_type
    }

    # relationships

    # functions
    def __repr__(self):
        return '<User {}, name: {} {}, email {}>'.format(self.username, self.firstname, self.lastname, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def hide_user(self):
        """Mark the user as hidden."""
        self.hidden = True
        db.session.commit()

    def delete_user(self):
        """Delete the user."""
        db.session.delete(self)
        db.session.commit()

class Teacher(User):
    __tablename__ = 'teacher'
    # traits
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    department : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(40))

    # auto-mapping for user type
    __mapper_args__ = {
        'polymorphic_identity' : 'Teacher',
    }

    # relationships
    sections: sqlo.WriteOnlyMapped['CourseSection'] = sqlo.relationship('CourseSection', back_populates='teacher')

    # functions
    def __repr__(self):
        return f'<Teacher {self.firstname} {self.lastname}, Department: {self.department}>'

    def get_sections(self):
        return db.session.scalars(self.sections.select()).all()

    def get_sections_query(self):
        return self.sections


class Student(User):
    __tablename__ = 'student'
    # traits
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)

    major : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(40))
    gpa : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    graduation_year : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)

    # auto-mapping for user type
    __mapper_args__ = {
        'polymorphic_identity' : 'Student',
    }

    # relationships
    enrolled: sqlo.WriteOnlyMapped['PastEnrollments'] = sqlo.relationship('PastEnrollments', back_populates='student')

    # functions
    def __repr__(self):
        return '<Student name {} {}, major {}, GPA {}, graduating in {} >'.format(self.firstname, self.lastname, self.major, self.gpa, self.graduation_year)

    def get_major(self):
        return self.major

    def get_enrollments(self):
        return db.session.scalars(self.enrolled.select()).all()


# Course model
class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    major: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(40), index=True)
    coursenum : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4), index=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(150))
    year : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4), index=True)

    hidden: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)  # Default is not hidden


    # relationships
    course_sections: sqlo.WriteOnlyMapped['CourseSection'] = sqlo.relationship('CourseSection', back_populates='course')
    course_enrolled: sqlo.WriteOnlyMapped['PastEnrollments'] = sqlo.relationship('PastEnrollments', back_populates='course')

    # methods
    def __repr__(self):
        return '<Course id: {} - coursenum: {} - title: {}>'.format(self.id, self.coursenum, self.title)

    def get_coursenum(self):
        return self.coursenum

    def get_title(self):
        return self.title
    
    def get_year(self):
        return self.year

    def get_sections(self):
        return db.session.scalars(self.course_sections.select()).all()  
    
    #id is the student's id
    def get_recommended_sections(self, sid):
        student = db.session.get(User, int(sid))
        recommended_sections = []
        past = db.session.scalars(sqla.select(PastEnrollments).where(PastEnrollments.course_id == self.id and PastEnrollments.student_id == sid)).first()
        sections = db.session.scalars(self.course_sections.select()).all()

        #print(sections)
        for section in sections:
            if float(student.gpa) >= float(section.min_gpa):
                # print(section)
                # print(past.grade)
                if past.grade == 'a':
                    # print("a")
                    recommended_sections.append(section)
                elif past.grade == 'b' and (section.min_grade == 'b' or section.min_grade == 'c'):
                    # print("B")
                    recommended_sections.append(section)
                elif past.grade == 'c' and section.min_grade == 'c':
                    # print("c")
                    recommended_sections.append(section)
        return recommended_sections
            
    def get_applied_sections(self, sid):
    # Fetch the student record
        student = db.session.get(User, int(sid))
        if not student:
            return []  
        applications = db.session.scalars(
            sqla.select(CourseApplication).where(
                (CourseApplication.course_id == self.id) &
                (CourseApplication.student_id == sid)
            )
        ).all()
        applied_sections = [app.section for app in applications if app.section]
        
        return applied_sections


    def get_sections_query(self):
        return self.course_sections  
    
    
    def get_sections_count(self):
        """Returns the count of sections for this course."""
        return len(self.get_sections())

    def hide_course(self):
        """Mark the course as hidden."""
        self.hidden = True
        db.session.commit()

    def delete_course(self):
        """Delete the course and related sections."""
        db.session.delete(self)
        db.session.commit()


# Past Enrollments model
class PastEnrollments(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id))
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id))
    grade : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1))

    sa_before = db.Column(db.Boolean, default=False)  # True if the student has been an SA before

    # relationships
    course : sqlo.Mapped[Course] = sqlo.relationship(back_populates = 'course_enrolled')
    student : sqlo.Mapped[Student] = sqlo.relationship(back_populates = 'enrolled')

    # methods
    def __repr__(self):
        return '<Student {} Course {} Grade {}>'.format(self.student, self.course, self.grade)

    

class CourseSection(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1))
    year: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(4))
    teacher_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Teacher.id), index=True)
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id), index=True)


    hidden: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False, nullable=True)  # Default is not hidden
    
    created_at: sqlo.Mapped[datetime] = sqlo.mapped_column( sqla.DateTime, default=datetime.utcnow, nullable=False)

    # SA traits
    num_sa: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    min_gpa: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    min_grade: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1))

    
    # Relationships
    course: sqlo.Mapped[Course] = sqlo.relationship('Course', back_populates='course_sections', cascade='save-update') 
    teacher: sqlo.Mapped[Teacher] = sqlo.relationship('Teacher', back_populates='sections')

    # Correct placement of delete-orphan on the "one" side of the relationship
    applications = db.relationship('CourseApplication', backref='section', cascade='all, delete')    
    
    def __repr__(self):
        return f'<CourseSection {self.course.title} Term: {self.term} Year: {self.year} - INFO: GPA {self.min_gpa}, GRADE: {self.min_grade}>'




class CourseApplication(db.Model):
    __tablename__ = 'course_applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)   
    section_id = db.Column(db.Integer, db.ForeignKey('course_section.id'))
    reason = db.Column(db.Text, nullable=False)  
    status = db.Column(db.String(50), default='pending')

    student = db.relationship('Student', backref='applications')
    course = db.relationship('Course', backref='applications')
    
    # Set single_parent=True to ensure that each CourseApplication references only one CourseSection
    def __repr__(self):
        return f'<CourseApplication {self.id} for student {self.student.username} to {self.course.title} section {self.section.id}>'

    # Custom validation method to ensure reason length is within limit
    @classmethod
    def validate_reason_length(cls, reason: str):
        if len(reason) > 200:
            raise ValueError("Reason must be under 200 characters.")



class EditApplicationForm(FlaskForm):
    reason = TextAreaField(
        'Reason for Application', 
        validators=[
            DataRequired(message="Please provide a reason."),
            Length(max=200, message="Reason must be under 200 characters.")
        ]
    )
    submit = SubmitField('Update Application')



class AcceptedStudent(db.Model):
    __tablename__ = 'accepted_students'
    
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  
    section_id = db.Column(db.Integer, db.ForeignKey('course_section.id'), nullable=False)  # Fix the reference here
    
    student = db.relationship('Student', backref=db.backref('accepted_sections', lazy=True))
    section = db.relationship('CourseSection', backref=db.backref('accepted_students', lazy=True))  # Correct model reference

    def __repr__(self):
        return f'<AcceptedStudent {self.student_id} - {self.section_id}>'