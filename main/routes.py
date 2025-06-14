from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from models import Schueler, Slot, db
from datetime import date, datetime

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    anzahl_schueler = Schueler.query.count()
    heute = date.today().strftime("%d.%m.%Y")

    return render_template("main/dashboard.html", anzahl_schueler=anzahl_schueler, heute=heute)

# Kalenderansicht
@main_bp.route("/calendar")
def calendar():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("main/calendar.html")

# Slots als JSON (optional nach Datum filterbar)
@main_bp.route("/calendar/slots")
def calendar_slots():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    date_filter = request.args.get('date')
    query = Slot.query
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(Slot.date == filter_date)
        except ValueError:
            pass  # Falsches Format ignorieren
    
    slots = query.all()
    return jsonify([
        {
            "id": slot.id,
            "date": slot.date.strftime("%Y-%m-%d"),
            "time": slot.time.strftime("%H:%M"),
            "status": slot.status
        } for slot in slots
    ])

# Slot buchen
@main_bp.route("/calendar/book", methods=["POST"])
def book_slot():
    if "user_id" not in session:
        return jsonify({"message": "Nicht eingeloggt"}), 401

    slot_id = request.json.get("slot_id")
    slot = Slot.query.get_or_404(slot_id)

    if slot.status != "frei":
        return jsonify({"message": "Slot bereits gebucht"}), 400

    slot.status = "gebucht"
    db.session.commit()
    return jsonify({"message": "Slot erfolgreich gebucht"})
