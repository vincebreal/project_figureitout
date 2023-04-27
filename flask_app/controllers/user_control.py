from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.figure_model import ActionFigure
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/registration_page')
def reg_page():
    return render_template('register.html')

@app.route('/login_page')
def logging_in():
    return render_template('log_in.html')


@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/registration_page')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    print(request.form)

    return redirect('/dashboard')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login_page')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data), figures_table=ActionFigure.get_all())


@app.route('/figureitout/myaccount')
def myaccount():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("my_account.html",user=User.get_by_id(data), figures_table=ActionFigure.get_all())


@app.route('/figureitout/edit_account')
def edit_account():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("edit_account.html",user=User.get_by_id(data))

@app.route('/figureitout/update_user', methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.update_validation(request.form):
        return redirect('/figureitout/edit_account')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    User.update_user_info(data)
    return redirect('/figureitout/myaccount')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')