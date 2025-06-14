from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required
from app import db
from models import Slot
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

@main.route('/calendar')
@login_required
def calendar():
    return render_template('main/calendar.html')

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
            pass
    slots = query.order_by(Slot.datum, Slot.uhrzeit).all()
    result = [{
        "id": s.id,
        "date": s.datum.strftime('%d.%m.%Y'),
        "time": s.uhrzeit.strftime('%H:%M'),
        "status": "frei" if not s.vergeben else "gebucht",
        "simulator": s.simulator
    } for s in slots]
    return jsonify(result)

@main.route('/calendar/book', methods=['POST'])
@login_required
def book_slot():
    data = request.get_json()
    slot_id = data.get("slot_id")
    slot = Slot.query.get(slot_id)
    if not slot:
        return jsonify({"message": "Slot nicht gefunden."}), 404
    if slot.vergeben:
        return jsonify({"message": "Slot bereits vergeben."}), 400
    slot.vergeben = True
    db.session.commit()
    return jsonify({"message": "Slot erfolgreich gebucht!"})
