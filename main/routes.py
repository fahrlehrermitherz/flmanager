from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Slot
from datetime import datetime

main = Blueprint('main', __name__)

# Startseite -> leitet direkt zum Login (oder Dashboard, wenn du willst)
@main.route('/')
def index():
    return redirect(url_for('auth.login'))

# Dashboard-Ansicht
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

# Kalender-Ansicht
@main.route('/calendar')
@login_required
def calendar():
    return render_template('main/calendar.html')

# API: Slots abrufen (mit optionalem Datumsfilter)
@main.route('/calendar/slots')
@login_required
def get_slots():
    date_filter = request.args.get('date')
    query = Slot.query

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(Slot.datum == filter_date)
        except ValueError:
            return jsonify({"message": "Ungültiges Datumsformat. Bitte YYYY-MM-DD verwenden."}), 400

    slots = query.order_by(Slot.datum, Slot.uhrzeit).all()

    result = [{
        "id": slot.id,
        "date": slot.datum.strftime('%d.%m.%Y'),
        "time": slot.uhrzeit.strftime('%H:%M'),
        "status": "frei" if not slot.vergeben else "gebucht",
        "simulator": slot.simulator
    } for slot in slots]

    return jsonify(result)

# API: Slot buchen
@main.route('/calendar/book', methods=['POST'])
@login_required
def book_slot():
    data = request.get_json()
    slot_id = data.get("slot_id")

    if not slot_id:
        return jsonify({"message": "Slot-ID fehlt."}), 400

    slot = Slot.query.get(slot_id)

    if not slot:
        return jsonify({"message": "Slot nicht gefunden."}), 404

    if slot.vergeben:
        return jsonify({"message": "Slot bereits vergeben."}), 400

    slot.vergeben = True
    db.session.commit()

    return jsonify({"message": "Slot erfolgreich gebucht!"})
