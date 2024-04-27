from flask import Flask, jsonify, Response, request, redirect, url_for, render_template
from markupsafe import escape
from flask import render_template
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Column, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
import json
from database.dbemployee import DBEmployee
from database.dbuser import DBUser
import logging
import os
from .authentic.auth import auth


SECRET_KEY = os.urandom(32)

# class LoginForm(FlaskForm):
#     email = StringField(label='Email', validators=[DataRequired()])
#     password = PasswordField(label='Password', validators=[DataRequired()])
#     submit = SubmitField(label='Log In')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.session_cookie_name = None

Base = declarative_base()

# Define the PostgreSQL URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://bdinh:linh1982@localhost:5432/company'

# create the extension
db = SQLAlchemy(model_class=Base)

# initialize the app with extension
db.init_app(app)

# initialize auth_blueprint
app.register_blueprint(auth)

@app.route("/list_employee")
def list_employee():
    employees = db.session.execute(db.select(DBEmployee).order_by(DBEmployee.employee_id)).scalars() 
    app.logger.info("Inside list employee")
    return render_template('employee.html', my_empl=employees)

@app.route("/list_employee_json", methods=['GET'])
def list_employee_json():
    if request.method == 'GET':
        employees = db.session.execute(db.select(DBEmployee).order_by(DBEmployee.employee_id)).scalars()
        json_data = [u._asdict() for u in employees]
        json_output = json.dumps(json_data)
        return json_output


@app.route("/add_employee", methods=['POST', 'GET'])
def add_employee():
    if request.method == "POST":    
        emp_id = None
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        manager_id = request.form["manageid"]  
        new_emp = DBEmployee(emp_id, firstname, lastname, manager_id)       
        db.session.add(new_emp)
        db.session.commit()
        # return redirect(url_for("user_detail", id=user.id))
        return redirect(url_for('success', name=firstname))
    elif request.method == "GET":
        return render_template('add_employee.html')

@app.route("/edit_employee/<employee_id>",methods=['POST','GET'])
def edit_employee(employee_id):
    emp_rec = db.get_or_404(DBEmployee,employee_id)

    if request.method == "POST":   
        app.logger.info('%s Edit employee data from database using Post method')    
        emp_rec.first_name = request.form.get("firstname")
        emp_rec.last_name = request.form.get("lastname")
        emp_manager_id = request.form.get("manageid")
        app.logger.info('%s Edit employee data from database using Post method')
        db.session.commit()
        return redirect(url_for('list_employee'))
    elif request.method == "GET":
        app.logger.info('%s Edit employee data from database using Get method')  
        emp_id = employee_id
        return render_template('edit_employee.html', emp_id=emp_id)

@app.route("/del_employee/<employee_id>",methods=['POST','GET'])
def del_employee(employee_id):
    emp_rec = db.get_or_404(DBEmployee,employee_id)

    if request.method == "GET":   
        db.session.delete(emp_rec)
        db.session.commit()
        app.logger.info('%s Delete employee data from database using GET method')
        db.session.commit()
        return redirect(url_for('list_employee'))
    elif request.method == "POST":
        app.logger.info('%s Delete employee data from database using POST method') 
    #     emp_id = employee_id
        return redirect(url_for('list_employee'))

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route('/api/<name>')
def api(name):
    return render_template('home.html', name=name)

@app.route("/login", methods=['POST', 'GET'])
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

@app.route("/register", methods=['POST', 'GET'])
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


if __name__ == "__main__":
    import logging
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "/home/bdinh/Hello_Flask/global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("/home/bdinh/Hello_Flask/global.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(debug=True)