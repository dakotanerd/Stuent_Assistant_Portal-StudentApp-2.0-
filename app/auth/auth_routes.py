from app import db
from flask import render_template, flash, redirect, url_for, session, request
import sqlalchemy as sqla
import identity.web
from app.main.models import User, Student, Teacher
from app.auth.auth_forms import  StudentRegistrationForm,TeacherRegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from app.auth import auth_blueprint as auth
from config import Config as appconfig

ssoauth = identity.web.Auth(
    session=session,
    authority=appconfig.AUTHORITY,
    client_id=appconfig.CLIENT_ID,
    client_credential=appconfig.CLIENT_SECRET
)
@auth.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        if current_user.user_type == 'Student':
            return redirect(url_for('main.student_index'))
        if current_user.user_type == 'Teacher':
            return redirect(url_for('main.teacher_index'))

    rform = StudentRegistrationForm()
    if rform.validate_on_submit():
        student = Student(username=rform.username.data,
                          firstname=rform.firstname.data,
                          lastname=rform.lastname.data,
                          email=rform.email.data,
                          wpi_id=rform.wpi_id.data,
                          phone=rform.phone.data,
                          major=rform.major.data,
                          gpa=rform.gpa.data,
                          graduation_year=rform.grad_year.data
                          )
        student.set_password(rform.password.data)
        db.session.add(student)
        try:
            db.session.commit()
            flash('Congratulations, you have been registered as a student!', 'success')
            return redirect(url_for('main.student_index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.', 'danger')
   
    return render_template('student_register.html', form = rform)

@auth.route('/teacher/register', methods=['GET', 'POST'])
def teacher_register():
    if current_user.is_authenticated:
        if current_user.user_type == 'Student':
            return redirect(url_for('main.student_index'))
        if current_user.user_type == 'Teacher':
            return redirect(url_for('main.teacher_index'))
    
    rform = TeacherRegistrationForm()
    if rform.validate_on_submit():
        teacher = Teacher(username=rform.username.data,
                          firstname=rform.firstname.data,
                          lastname=rform.lastname.data,
                          wpi_id=rform.wpi_id.data,
                          email=rform.email.data,
                          phone=rform.phone.data,
                          department=rform.department.data,
                          )
        teacher.set_password(rform.password.data)
        db.session.add(teacher)
        try:
            db.session.commit()
            flash('Congratulations, you have been registered as a teacher!', 'success')
            return redirect(url_for('main.teacher_index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.', 'danger')
   
    return render_template('teacher_register.html', form = rform)


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/user/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'Student':
            return redirect(url_for('main.student_index'))
        if current_user.user_type == 'Teacher':
            return redirect(url_for('main.teacher_index'))
   
    lform = LoginForm()
    if lform.validate_on_submit():
        user = db.session.scalars(sqla.select(User).where(User.username == lform.username.data)).first()


        if user is None or not user.check_password(lform.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))


        if user.user_type == 'Student':
            login_user(user, remember=lform.remember_me.data)
            flash(f"Student User: {current_user.username} has successfully logged in!", 'success')
            return redirect(url_for('main.student_index'))
        
        if user.user_type == 'Teacher':
            login_user(user, remember=lform.remember_me.data)
            flash(f"Teacher User: {current_user.username} has successfully logged in!", 'success')
            return redirect(url_for('main.teacher_index'))
   
    return render_template('login.html', form=lform)

@auth.route('/student/logout', methods=['GET'])
@login_required
def logout():
    if session.get('ssologin') is not None:
        ssoauth.log_out(url_for("auth.login", _external=True))
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/ssologin")
def ssologin():
    return render_template("SSO.html", **ssoauth.log_in(
        scopes=appconfig.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth.auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))
@auth.route('/getAToken')
def auth_response():
    result = ssoauth.complete_log_in(request.args)
    if "error" in result:
        flash('SSO Login Failed, try again')
        return redirect(url_for('auth.login'))

    user = db.session.scalars(sqla.select(User).where(User.email == ssoauth.get_user()["preferred_username"])).first()
    login_user(user, remember=False)
    session['sso']=ssoauth.get_user()["preferred_username"]
    if user.user_type == 'Student':
        flash(f'Student user {current_user.username} has successfully logged in!')
        return redirect(url_for('main.student_index'))
        
    if user.user_type == 'Teacher':
        flash(f'Teacher user {current_user.username} has successfully logged in!')
        return redirect(url_for('main.teacher_index'))
    