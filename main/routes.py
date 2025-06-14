from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from models import db, Slot
from datetime import datetime

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Beispiel-Zähler oder Inhalte, wie schon vorhanden
    return render_template("main/dashboard.html")

@main_bp.route("/calendar")
@login_required
def calendar():
    return render_template("main/calendar.html")

@main_bp.route("/calendar/slots")
@login_required
def get_slots():
    slots = Slot.query.order_by(Slot.datum, Slot.uhrzeit).all()
    result = []
    for s in slots:
        result.append({
            "id": s.id,
            "date": s.datum.strftime('%d.%m.%Y'),
            "time": s.uhrzeit.strftime('%H:%M'),
            "status": s.status
        })
    return jsonify(result)

@main_bp.route("/calendar/book", methods=["POST"])
@login_required
def book_slot():
    data = request.get_json()
    slot_id = data.get("slot_id")
    slot = Slot.query.get(slot_id)
    if not slot:
        return jsonify({"message": "Slot nicht gefunden."}), 404
    if slot.status != "frei":
        return jsonify({"message": "Slot nicht buchbar."}), 400
    
    slot.status = "reserviert"
    db.session.commit()
    return jsonify({"message": "Slot erfolgreich gebucht!"})
