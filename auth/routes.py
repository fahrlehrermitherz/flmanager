from flask import Blueprint, render_template, redirect, url_for, flash, request, session
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
        flash('⚠️ Du bist bereits eingeloggt.', 'info')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwort, password):
            login_user(user)
            session["user_id"] = user.id
            session["rolle"] = user.rolle.name
            session["name"] = f"{user.vorname} {user.nachname}"
            flash('✅ Login erfolgreich.', 'success')

            # Weiterleiten zur ursprünglich angeforderten Seite oder Dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('❌ Ungültige Zugangsdaten.', 'danger')

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('🚪 Du wurdest ausgeloggt.', 'info')
    return redirect(url_for('auth.login'))
