from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from models import db, Slot
from datetime import datetime
import csv
from io import StringIO

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/dashboard")
@login_required
def dashboard():
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
            "date": s.datum.strftime('%Y-%m-%d'),
            "time": s.uhrzeit.strftime('%H:%M'),
            "status": "vergeben" if s.vergeben else "frei",
            "simulator": s.simulator,
            "fahrlehrer": f"{s.fahrlehrer.vorname} {s.fahrlehrer.nachname}" if s.fahrlehrer else "-"
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
    if slot.vergeben:
        return jsonify({"message": "Slot nicht buchbar."}), 400

    slot.vergeben = True
    slot.schueler_id = current_user.id  # Wenn Fahrschüler-Login
    db.session.commit()
    return jsonify({"message": "Slot erfolgreich gebucht!"})

@main_bp.route("/calendar/export")
@login_required
def export_slots():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slots = Slot.query.order_by(Slot.datum, Slot.uhrzeit).all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Datum", "Uhrzeit", "Status", "Simulator", "Fahrlehrer"])

    for s in slots:
        writer.writerow([
            s.datum.strftime('%Y-%m-%d'),
            s.uhrzeit.strftime('%H:%M'),
            "vergeben" if s.vergeben else "frei",
            "Ja" if s.simulator else "Nein",
            f"{s.fahrlehrer.vorname} {s.fahrlehrer.nachname}" if s.fahrlehrer else "-"
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=slots.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main_bp.route("/calendar/slot/<int:slot_id>", methods=["GET", "POST"])
@login_required
def edit_slot(slot_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slot = Slot.query.get_or_404(slot_id)
    if request.method == "POST":
        try:
            slot.datum = datetime.strptime(request.form.get("datum"), "%Y-%m-%d").date()
            slot.uhrzeit = datetime.strptime(request.form.get("uhrzeit"), "%H:%M").time()
            slot.simulator = bool(request.form.get("simulator"))
            db.session.commit()
            flash("Slot aktualisiert", "success")
            return redirect(url_for("main.calendar"))
        except Exception:
            flash("Fehler beim Speichern", "danger")
    return render_template("main/slot_form.html", slot=slot)
