from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db, login_manager
from models import User
from forms import LoginForm  # Wichtig: wir nutzen jetzt eine FlaskForm

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.passwort, password):
            login_user(user)
            session["user_id"] = user.id
            session["rolle"] = user.rolle.name
            session["name"] = f"{user.vorname} {user.nachname}"
            flash('✅ Login erfolgreich!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('❌ Login fehlgeschlagen! Prüfe deine Daten.', 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('🚪 Du bist abgemeldet.', 'info')
    return redirect(url_for('auth.login'))
