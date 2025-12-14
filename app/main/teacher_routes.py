from app import db
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sqla
from app.main.models import AcceptedStudent, CourseApplication, PastEnrollments, User, Student, Teacher, Course, CourseSection
from app.main.forms import SectionForm
from flask_login import login_user, current_user, logout_user, login_required
from app.main import main_blueprint as main
from sqlalchemy.orm import aliased

# Helper function to ensure that only teachers have access to certain routes
def ensure_teacher():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    if current_user.user_type == "Student":
        flash('You do not have access to that page!', 'danger')
        return redirect(url_for('main.student_index'))

@main.route('/teacher/index', methods=['GET'])
@login_required
def teacher_index():
    check = ensure_teacher()
    if check:
        return check

    # Fetch all sections taught by the teacher
    sections = db.session.scalars(
        sqla.select(CourseSection).where(CourseSection.teacher_id == current_user.id)).all()

    section_details = []
    for section in sections:
        course = db.session.get(Course, section.course_id)

        # Fetch all applications for this section
        applications = db.session.scalars(
            sqla.select(CourseApplication)
            .where(CourseApplication.section_id == section.id)
            .where(CourseApplication.status != 'rejected')  # Exclude rejected applications
        ).all()

        # Fetch all students who are accepted into any section, not limited to the same course
        accepted_students = db.session.scalars(
            sqla.select(Student.id)
            .join(AcceptedStudent, AcceptedStudent.student_id == Student.id)  # Join with AcceptedStudent to get the accepted students
            .join(CourseSection, AcceptedStudent.section_id == CourseSection.id)  # Join with CourseSection
            .filter(AcceptedStudent.section_id != section.id)  # Exclude students already accepted in the current section
        ).all()

        # Add details for each section and its applications
        section_details.append({
            'course': course,
            'section': section,
            'applications': applications,
            'accepted_student_ids': accepted_students  # List of student IDs accepted in any section
        })

    return render_template(
        'teacher_index.html',
        title="Teacher Home Page",
        sections=section_details
    )


@main.route('/course/section/create', methods=['GET', 'POST'])
@login_required
def create_section():
    check = ensure_teacher()
    if check:
        return check

    sform = SectionForm()
    
    if request.method == 'POST' and sform.validate_on_submit():
        course = db.session.get(Course, sform.course.data.id)
        if not course:
            flash('Course not found!', 'danger')
            return redirect(url_for('main.create_section'))
        
        if sform.min_gpa.data < 0 or sform.min_gpa.data > 4:
            flash("GPA must be between 0 and 4.", "danger")
        else:
            # Create a new course section
            new_section = CourseSection(
                term=sform.term.data,
                year=sform.year.data,
                teacher_id=current_user.id,
                course_id=sform.course.data.id,
                num_sa=sform.sa_num.data,
                min_gpa=sform.min_gpa.data,
                min_grade=sform.min_grade.data
            )

            db.session.add(new_section)
            db.session.commit()

        flash('Your section has been successfully created', 'success')
        return redirect(url_for('main.teacher_index'))

    return render_template('create.html', form=sform)

@main.route('/teacher/profile', methods=['GET'])
@login_required
def display_Teacher_profile():
    check = ensure_teacher()
    if check:
        return check

    # Fetch sections for the teacher
    sections = db.session.scalars(sqla.select(CourseSection).where(CourseSection.teacher_id == current_user.id)).all()

    # Gather more details about each section, such as course name, term, etc.
    section_details = []
    for section in sections:
        course = db.session.get(Course, section.course_id)
        section_details.append({
            'course': course,
            'section': section,
            'term': section.term,
            'year': section.year
        })

    return render_template('display_teacher_profile.html', title="Teacher Profile", section_details=section_details)

# Route to Update Application Status
@main.route('/teacher/application/update/<int:application_id>', methods=['POST'])
@login_required
def update_application_status(application_id):
    # Fetch the application
    application = db.session.get(CourseApplication, application_id)
    if not application:
        flash("Application not found.", "danger")
        return redirect(url_for('main.teacher_index'))

    # Check if the current user is the teacher for the section
    if application.section.teacher_id != current_user.id:
        flash("You do not have permission to update this application.", "danger")
        return redirect(url_for('main.teacher_index'))

    # Update the application status based on form data
    new_status = request.form.get('status')

    if new_status == 'accepted':
        # Check if the maximum number of accepted students has been reached
        section = application.section
        current_sa_count = db.session.query(CourseApplication).filter_by(
            section_id=section.id,
            status='accepted'
        ).count()
        max_sas = section.num_sa

        if current_sa_count >= max_sas:
            flash(f"Cannot accept more students. The maximum number of SAs ({max_sas}) for this section has been reached.", "danger")
        else:
            # Update the application status and add to AcceptedStudent table
            application.status = 'accepted'

            # Check if already in AcceptedStudent, otherwise add
            existing_entry = db.session.query(AcceptedStudent).filter_by(
                student_id=application.student_id,
                section_id=application.section_id
            ).first()
            if not existing_entry:
                accepted_student = AcceptedStudent(
                    student_id=application.student_id,
                    section_id=application.section_id
                )
                db.session.add(accepted_student)

            # Delete all other pending applications for this student
            db.session.query(CourseApplication).filter(
                CourseApplication.student_id == application.student_id,
                CourseApplication.status == 'pending'
            ).delete()

            db.session.commit()
            flash(f"The selected student's application has been accpted, the status has been removed", "success")

    elif new_status in ['pending', 'rejected']:
        # Update the application status and ensure removal from AcceptedStudent table
        application.status = new_status

        # Remove the student from the AcceptedStudent table
        db.session.query(AcceptedStudent).filter_by(
            student_id=application.student_id,
            section_id=application.section_id
        ).delete()

        db.session.commit()
        flash(f"Current student application status updated to {new_status}.", "success")
    else:
        flash("Invalid status.", "danger")

    return redirect(url_for('main.teacher_index'))



@main.route('/teacher/section/<int:section_id>/applications', methods=['GET'])
@login_required
def view_section_applications(section_id):
    # Fetch applications for the specific section, excluding rejected applications
    applications = db.session.scalars(
        sqla.select(CourseApplication)
        .where(CourseApplication.section_id == section_id)
        .where(CourseApplication.status != 'rejected')  
    ).all()
    return render_template('view_section_applications.html', applications=applications)

@main.route('/view_profile/<int:student_id>')
@login_required
def view_profile(student_id):
    student = User.query.get_or_404(student_id)
    applications = CourseApplication.query.filter_by(student_id=student.id).all()
    enrollments = PastEnrollments.query.filter_by(student_id=student.id).all()
    return render_template('view_profile.html', student=student, applications=applications, enrollments=enrollments)

@main.route('/teacher/edit_course/<int:section_id>', methods=['GET', 'POST'])
@login_required
def teacher_edit_course(section_id):
    section = CourseSection.query.get_or_404(section_id)

    # Ensure the user is the teacher for the section
    if section.teacher_id != current_user.id:
        flash("You do not have permission to edit this section.", "danger")
        return redirect(url_for('main.teacher_index'))

    if request.method == 'POST':
        # Handle the form submission and update the section
        title = request.form.get('title')
        coursenum = request.form.get('coursenum')
        year = request.form.get('year')
        term = request.form.get('term')
        sa_num = request.form.get('sa_num')

        # Update the course information (this is the correct way to update the Course model)
        section.course.title = title
        section.course.coursenum = coursenum

        # Update the section information
        section.year = year
        section.term = term
        section.num_sa = sa_num  # Fixing variable name, it was `sa_num` in the form, update it accordingly in the section model.

        # Commit the changes to the database
        db.session.commit()

        flash('Course updated successfully!', 'success')
        return redirect(url_for('main.teacher_index'))

    # If GET request, render the form with current course details
    return render_template('teacher_edit_course.html', section=section)

@main.route('/delete_section/<int:section_id>', methods=['POST'])
@login_required
def teacher_delete_section(section_id):
    section = db.session.query(CourseSection).options(sqla.orm.joinedload(CourseSection.course)).get_or_404(section_id)

    # Ensure the section belongs to the teacher
    if section.teacher_id != current_user.id:
        flash("You do not have permission to delete this section.", "danger")
        return redirect(url_for('main.teacher_index'))

    try:
        # Cache the course title before deletion
        course_title = section.course.title

        # Delete all AcceptedStudent entries related to the section
        accepted_students = db.session.scalars(
            sqla.select(AcceptedStudent).where(AcceptedStudent.section_id == section.id)
        ).all()
        for accepted_student in accepted_students:
            db.session.delete(accepted_student)

        # Delete all applications associated with the section
        applications = db.session.scalars(
            sqla.select(CourseApplication)
            .where(CourseApplication.section_id == section.id)
        ).all()
        for application in applications:
            db.session.delete(application)

        # Now delete the section
        db.session.delete(section)
        db.session.commit()

        # Check if there are other sections for the same course
        remaining_sections = CourseSection.query.filter_by(course_id=section.course_id).count()
        if remaining_sections == 0:
            flash(f"Section deleted. No other sections remain for the course '{course_title}'.", "success")
        else:
            flash(f"Section deleted successfully.", "success")

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        flash(f"An error occurred while deleting the section: {str(e)}", "danger")

    return redirect(url_for('main.teacher_index'))

