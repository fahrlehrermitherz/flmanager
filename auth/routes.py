from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db, login_manager
from models import User

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.passwort, password):
            login_user(user)
            flash('Login erfolgreich!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login fehlgeschlagen!', 'danger')

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du bist abgemeldet.', 'info')
    return redirect(url_for('auth.login'))
