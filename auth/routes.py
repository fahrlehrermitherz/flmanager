from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db, login_manager
from models import User

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    print(f"🔍 load_user aufgerufen mit user_id: {user_id}")
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(f"ℹ️ Bereits eingeloggt: {current_user.id}")
        flash('⚠️ Du bist bereits eingeloggt.', 'info')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"📩 POST empfangen: email={email}, password={password}")

        user = User.query.filter_by(email=email).first()
        print(f"👤 Gefundener User: {user}")
        
        if user:
            print(f"🔑 Vergleich Passwort-Hash für User ID {user.id}")
            password_check = check_password_hash(user.passwort, password)
            print(f"✅ Passwortprüfung Ergebnis: {password_check}")
        else:
            print("❌ Kein User mit dieser E-Mail gefunden")

        if user and check_password_hash(user.passwort, password):
            login_user(user)
            session["user_id"] = user.id
            session["rolle"] = user.rolle.name
            session["name"] = f"{user.vorname} {user.nachname}"
            flash('✅ Login erfolgreich.', 'success')

            next_page = request.args.get('next')
            print(f"➡️ Weiterleitung zu: {next_page if next_page else '/dashboard'}")
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('❌ Ungültige Zugangsdaten.', 'danger')

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    print(f"👋 User {current_user.id} logged out.")
    logout_user()
    session.clear()
    flash('🚪 Du wurdest ausgeloggt.', 'info')
    return redirect(url_for('auth.login'))
