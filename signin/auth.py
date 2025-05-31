from flask import request, redirect, url_for, render_template, Blueprint
from database.dbuser import DBUser
from .loginform import LoginForm, RegisterForm
from werkzeug.security import *
from extensions import db

auth_ab = Blueprint('auth', __name__,  template_folder='templates',static_folder='static', url_prefix='/auth')
    
@auth_ab.route('/printme')
def printme():
    return "<h1>helloworld</h1>"

@auth_ab.route('/logout1')
def logout1():
    return 'Logout'

@auth_ab.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm(csrf_enabled=True)
    if request.method == "POST":
        if login_form.validate_on_submit():

            email = login_form.email.data
            password = login_form.password.data

            result = db.session.execute(db.select(DBUser).where(DBUser.email == email))
            user = result.scalar()

            if check_password_hash(user.password,password):
                app.logger.info('%s Validate Username and Password Post method')
                return redirect(url_for('list_employee'))
            else:
                app.logger.info('%s InValid Username and Password Post method',)
                return render_template('login.html', form=login_form)
    elif request.method == "GET":
        return render_template('login.html', form=login_form)

@auth_ab.route('/register', methods=['POST', 'GET'])
def register():
    login_form = RegisterForm(csrf_enabled=True)
    if request.method == "POST":
        hashing_and_salted_pass = generate_password_hash (request.form.get('password'),method='pbkdf2:sha256',salt_length=8)

        new_user = DBUser(id=None,
                          email=request.form.get('email'),
                          password=hashing_and_salted_pass,
                          name=request.form.get('name'))
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html', form=login_form)
    elif request.method == "GET":
        return render_template('register.html', form=login_form)
