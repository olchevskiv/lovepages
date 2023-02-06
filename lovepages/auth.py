from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, User_Login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        user_agent = request.headers.get('User-Agent')
        remote_ip = request.remote_addr

        user = User.query.filter(User.user_name==user_name).first()
        if user:
            if check_password_hash(user.password, password):
                user_login = User_Login(user_name=user_name, ip=remote_ip, user_agent=user_agent, success=True)
                db.session.add(user_login)
                db.session.commit()
                login_user(user, remember=True)
                flash('yay', category="success")
                return redirect(url_for('views.home'))
            else:
                user_login = User_Login(user_name=user_name, ip=remote_ip, user_agent=user_agent, success=False)
                db.session.add(user_login)
                db.session.commit()
                flash('Incorrecto password', category="error")
        else:
            user_login = User_Login(user_name=user_name, ip=remote_ip, user_agent=user_agent, success=False)
            db.session.add(user_login)
            db.session.commit()
            flash('An account with this user name doesnt exist friend', category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        display_name =  request.form.get('display_name')
        birth_date = request.form.get('birth_date')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if len(email) < 4:
            flash('Invalid email', category="error")
        elif len(user_name) < 2:
            flash('Invalid user name', category="error")
        elif len(password) < 12:
            flash('Invalid pass', category="error")
        elif len(display_name) < 2:
            flash('Invalid display name', category="error")
        elif confirm_password != password:
            flash('Passwords dont match', category="error")
        else:
            check_user = User.query.filter((User.email==email) | (User.user_name==user_name)).first()
            if check_user:
                flash('Non unique email or username', category="error")
            else:
                new_user = User(email=email, user_name=user_name, display_name=display_name, birthdate= datetime.strptime(birth_date, "%Y-%m-%d"), password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                db.session.add(new_user)
                return redirect(url_for('views.home'))


    return render_template("signup.html", user=current_user)


