from app import db
from flask import flash, render_template, redirect, request, url_for
import sqlalchemy as sqla

from app.main.forms import SectionForm, StudentCourseForm, EditStudentProfileForm
from app.main.models import Course, EditApplicationForm, PastEnrollments, CourseSection, CourseApplication, AcceptedStudent
from flask_login import current_user, login_required
from app.main import main_blueprint as main


def ensure_student():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    if current_user.user_type == "Teacher":
        flash('You do not have access to that page!', 'danger' )
        return redirect(url_for('main.teacher_index'))


# Assuming you have a model for AcceptedStudent, you can query the AcceptedStudent table to get the sections the student is accepted to

from app.main.models import AcceptedStudent

@main.route('/student/index', methods=['GET'])
@login_required
def student_index():
    # Fetch all courses
    all_courses = db.session.scalars(sqla.select(Course)).all()

    # Get the sections the student has been accepted to
    accepted_sections = db.session.scalars(
        sqla.select(AcceptedStudent.section_id)
        .where(AcceptedStudent.student_id == current_user.id)
    ).all()

    # accepted_sections is a list of integers, no need for [0] here
    accepted_section_ids = {section_id for section_id in accepted_sections}

    # Get all the courses that the current student has applied for
    applied_courses = db.session.scalars(
        sqla.select(CourseApplication)
        .where(CourseApplication.student_id == current_user.id)
    ).all()

    applied_course_ids = {application.course_id for application in applied_courses}

    # Get the student's past enrollments to check for 'sa_before' status
    past_enrollments = db.session.scalars(
        sqla.select(PastEnrollments)
        .where(PastEnrollments.student_id == current_user.id)
    ).all()

    # Filter recommended courses based on GPA and SA (sa_before) status
    recommended_courses = [
        course for course in all_courses
        if any(
            # Check if the student's GPA meets the minimum GPA requirement
            float(current_user.gpa) >= float(section.min_gpa) and
            any(
                # Check if the student has taken this section in a past enrollment and was an SA
                course == past_enrollment.course and past_enrollment.sa_before
                for past_enrollment in past_enrollments
            )
            for section in course.get_sections()  # Iterate over sections of the course
        )
    ]

    # Exclude courses that the student has already applied for
    recommended_courses = [course for course in recommended_courses if course.id not in applied_course_ids]

    # Filter out the recommended courses from all courses to avoid showing duplicates
    all_courses_to_show = [
        course for course in all_courses
        #if course.id not in applied_course_ids and course.id not in [course.id for course in recommended_courses]
    ]
    # Pass accepted_section_ids to the template
    return render_template(
        'student_index.html',
        title="Student Home Page",
        recommended_courses=recommended_courses,
        courses=all_courses_to_show,  
        applied_courses=applied_courses,
        applied_course_ids=applied_course_ids,
        accepted_section_ids=accepted_section_ids  # Pass the accepted section IDs to the template
    )




@main.route('/student/application/<int:section_id>', methods=['GET', 'POST'])
@login_required
def application(section_id):
    # Fetch the section based on the ID
    section = db.session.get(CourseSection, section_id)
    if not section:
        flash("Section not found.", "danger")
        return redirect(url_for('main.student_index'))

    if request.method == 'POST':
        # Capture the reason for the application
        reason = request.form['reason']  # Only expect the reason

        # Create a new application
        application = CourseApplication(
            student_id=current_user.id,
            section_id=section.id,
            course_id=section.course.id, 
            reason=reason,
            status='pending'  # New applications are pending
        )
        try:
            db.session.add(application)
            db.session.commit()
            flash("Application submitted successfully!", "success")
        except Exception as e:
            db.session.rollback()  
            flash(f"Error submitting application: {e}", "danger")

        return redirect(url_for('main.student_index'))  

    # Render the application form if GET request
    return render_template('application.html', title="Course Application", section=section)


@main.route('/student/current_applications', methods=['GET'])
@login_required
def current_applications():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    # Fetch all applications for the current student
    applications = db.session.scalars(
        sqla.select(CourseApplication)
        .where(CourseApplication.student_id == current_user.id)
    ).all()

    # Check if the student has applied for any courses
    if not applications:
        flash("You have not applied for any courses yet.", "info")

    # Pass applications data to the template
    return render_template('current_application.html', applied_courses=applications)


@main.route('/student/profile', methods=['GET'])
@login_required
def display_Student_profile():
    # Get the student's applications
    applications = db.session.scalars(
        sqla.select(CourseApplication).where(CourseApplication.student_id == current_user.id)
    ).all()

    enrollments = db.session.scalars(sqla.select(PastEnrollments).where(PastEnrollments.student_id == current_user.id)).all()

    # Pass the applications to the template
    return render_template('display_student_profile.html', title="Student Profile", applications=applications, enrollments=enrollments)


@main.route('/student/course/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    if current_user.user_type == "Teacher":
        return redirect(url_for('main.teacher_index'))
    
    scForm = StudentCourseForm()

    if request.method == 'POST':
        # Create the enrollment object and check if the checkbox for 'sa_before' was checked
        enrollment = PastEnrollments(
            student_id=current_user.id,
            course_id=scForm.course.data.id,
            grade=scForm.grade.data,
            sa_before=scForm.sa_before.data  # This will capture the boolean value of the checkbox
        )
        try:
            db.session.add(enrollment)
            db.session.commit()

            flash('Your past enrollment has been successfully added!', 'success')
            return redirect(url_for('main.display_Student_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding enrollment: {e}", 'danger')

    return render_template('past_course.html', title="Add Past Enrollment", form=scForm)


@main.route('/student/applications', methods=['GET'])
@login_required
def view_applications():
    # Fetch all applications for the current student
    applications = db.session.scalars(
        sqla.select(CourseApplication).where(CourseApplication.student_id == current_user.id)
    ).all()

    return render_template('view_applications.html', applications=applications)


@main.route('/student/edit/profile', methods=['GET', 'POST'])
@login_required
def edit_student_profile():
    from app.main.models import Student  # Assuming you have a Student model
    student = db.session.get(Student, current_user.id)  # Fetch the logged-in student's profile
    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for('main.student_index'))

    form = EditStudentProfileForm()  # Use the form defined earlier
    if request.method == 'POST' and form.validate_on_submit():
        # Check if GPA is valid
        if form.gpa.data < 0 or form.gpa.data > 4:
            flash("GPA must be between 0 and 4.", "danger")
        else:
            # Update the student's profile based on form data
            try:
                student.firstname = form.firstname.data
                student.lastname = form.lastname.data
                student.email = form.email.data
                student.wpi_id = form.wpi_id.data
                student.phone = form.phone.data
                student.gpa = form.gpa.data

                db.session.commit()  # Save changes to the database
                flash("Profile updated successfully!", "success")
            except Exception as e:
                db.session.rollback()  # Rollback changes if there's an error
                flash(f"Error updating profile: {e}", "danger")

            return redirect(url_for('main.student_index'))  # Redirect to student index or dashboard

    # Pre-fill the form with existing data if GET request
    elif request.method == 'GET':
        form.firstname.data = student.firstname
        form.lastname.data = student.lastname
        form.email.data = student.email
        form.wpi_id.data = student.wpi_id
        form.phone.data = student.phone
        form.gpa.data = student.gpa

    return render_template('edit_student_profile.html', title="Edit Profile", form=form)


@main.route('/student/edit/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    # Fetch the application based on the ID
    application = db.session.get(CourseApplication, application_id)
    
    if not application:
        flash("Application not found.", "danger")
        return redirect(url_for('main.student_index'))

    # Ensure the logged-in student is the owner of the application
    if application.student_id != current_user.id:
        flash("You do not have permission to edit this application.", "danger")
        return redirect(url_for('main.student_index'))

    # Use the EditApplicationForm
    form = EditApplicationForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Perform length validation at the model level
        try:
            CourseApplication.validate_reason_length(form.reason.data)

            # Update the application details based on form input
            application.reason = form.reason.data

            # Commit the changes to the database
            db.session.commit()
            flash("Application updated successfully!", "success")

            return redirect(url_for('main.student_index'))  # Redirect to applications view page

        except ValueError as e:
            flash(f"Error: {e}", "danger")  # Flash the error message if validation fails
        except Exception as e:
            db.session.rollback()  # Rollback if any error occurs
            flash(f"Error updating application: {e}", "danger")

    # Pre-fill the form with the existing application data if GET request
    elif request.method == 'GET':
        form.reason.data = application.reason

    return render_template('edit_application.html', title="Edit Application", form=form, application=application)


from flask import redirect, url_for, request
from flask_login import login_required
from .models import CourseApplication

@main.route('/delete_application/<int:application_id>', methods=['POST'])
@login_required
def delete_application(application_id):
    # Query for the application by ID
    application = CourseApplication.query.get(application_id)
    
    # Ensure that the application exists
    if application:
        # Delete the application
        db.session.delete(application)
        db.session.commit()

    # Redirect back to the student's application list or another appropriate page
    return redirect(url_for('main.student_index'))


from flask import redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.main.models import PastEnrollments

@main.route('/student/delete_past_enrollment/<int:enrollment_id>', methods=['POST'])
@login_required
def delete_past_enrollment(enrollment_id):
    # Fetch the enrollment record by ID
    enrollment = PastEnrollments.query.get(enrollment_id)
    
    # Check if the enrollment exists and belongs to the current student
    if enrollment and enrollment.student_id == current_user.id:
        try:
            # Delete the enrollment
            db.session.delete(enrollment)
            db.session.commit()
            flash('Past enrollment deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"Error deleting past enrollment: {e}", 'danger')
    else:
        flash('You do not have permission to delete this past enrollment.', 'danger')
    
    # Redirect back to the student profile page
    return redirect(url_for('main.display_Student_profile'))

from flask import Flask