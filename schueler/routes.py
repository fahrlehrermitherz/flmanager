from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, make_response
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Schueler, Fahrstundenprotokoll, FahrstundenTyp
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

schueler_bp = Blueprint('schueler', __name__, url_prefix='/schueler')

# Fahrstunde anlegen
@schueler_bp.route('/fahrstunde/anlegen', methods=['GET', 'POST'])
@login_required
def fahrstunde_anlegen():
    schueler_list = Schueler.query.all()
    typen = FahrstundenTyp.query.all()

    if request.method == 'POST':
        try:
            schueler_id = request.form['schueler_id']
            typ_id = request.form['typ_id']
            datum = datetime.strptime(request.form['datum'], '%Y-%m-%d').date()
            uhrzeit = datetime.strptime(request.form['uhrzeit'], '%H:%M').time()
            dauer_minuten = int(request.form['dauer_minuten'])
            inhalt = request.form['inhalt']
            bezahlt = request.form['bezahlt']

            neue_fahrstunde = Fahrstundenprotokoll(
                schueler_id=schueler_id,
                fahrlehrer_id=current_user.id,
                typ_id=typ_id,
                datum=datum,
                uhrzeit=uhrzeit,
                dauer_minuten=dauer_minuten,
                inhalt=inhalt,
                bezahlt=bezahlt
            )

            db.session.add(neue_fahrstunde)
            db.session.commit()

            flash('✅ Fahrstunde erfolgreich angelegt.', 'success')
            return redirect(url_for('schueler_bp.fahrstunde_anlegen'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Fehler beim Anlegen: {e}', 'danger')

    return render_template('schueler/fahrstunde_anlegen.html', schueler=schueler_list, typen=typen)

# Kalenderdaten (JSON)
@schueler_bp.route('/fahrstunden/daten')
@login_required
def fahrstunden_daten():
    fahrstunden = Fahrstundenprotokoll.query.all()
    events = [{
        'title': f"{f.schueler.vorname} {f.schueler.nachname} - {f.typ.bezeichnung}",
        'start': datetime.combine(f.datum, f.uhrzeit).isoformat(),
        'end': (datetime.combine(f.datum, f.uhrzeit) + timedelta(minutes=f.dauer_minuten)).isoformat()
    } for f in fahrstunden]
    return jsonify(events)

# Schüler-Profil
@schueler_bp.route('/profil/<int:id>')
@login_required
def schueler_profil(id):
    schueler_obj = Schueler.query.get_or_404(id)
    fahrten = Fahrstundenprotokoll.query.filter_by(schueler_id=id)\
        .order_by(Fahrstundenprotokoll.datum.asc(), Fahrstundenprotokoll.uhrzeit.asc()).all()
    naechste_fahrt = Fahrstundenprotokoll.query.filter_by(schueler_id=id)\
        .filter(Fahrstundenprotokoll.datum >= datetime.utcnow().date())\
        .order_by(Fahrstundenprotokoll.datum.asc(), Fahrstundenprotokoll.uhrzeit.asc()).first()

    return render_template('schueler/profil.html', schueler=schueler_obj, fahrten=fahrten, naechste_fahrt=naechste_fahrt)

# PDF einer Fahrstunde
@schueler_bp.route('/fahrstunde/pdf/<int:fahrstunde_id>')
@login_required
def fahrstunde_pdf(fahrstunde_id):
    fahrt = Fahrstundenprotokoll.query.get_or_404(fahrstunde_id)
    schueler = fahrt.schueler

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Fahrstunden-Protokoll")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Schüler: {schueler.vorname} {schueler.nachname}")
    p.drawString(50, height - 120, f"Datum: {fahrt.datum.strftime('%d.%m.%Y')}")
    p.drawString(50, height - 140, f"Uhrzeit: {fahrt.uhrzeit.strftime('%H:%M')}")
    p.drawString(50, height - 160, f"Typ: {fahrt.typ.bezeichnung}")
    p.drawString(50, height - 180, f"Dauer: {fahrt.dauer_minuten} Minuten")
    p.drawString(50, height - 200, f"Bezahlt: {fahrt.bezahlt}")

    p.drawString(50, height - 240, "Inhalt / Notizen:")
    text = p.beginText(50, height - 260)
    text.setFont("Helvetica", 11)
    for line in fahrt.inhalt.splitlines():
        text.textLine(line)
    p.drawText(text)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Fahrstunde_{fahrt.id}.pdf'
    return response

# Sammel-PDF aller Fahrten
@schueler_bp.route('/profil/<int:schueler_id>/pdf')
@login_required
def schueler_fahrten_pdf(schueler_id):
    schueler = Schueler.query.get_or_404(schueler_id)
    fahrten = Fahrstundenprotokoll.query.filter_by(schueler_id=schueler_id)\
        .order_by(Fahrstundenprotokoll.datum.asc(), Fahrstundenprotokoll.uhrzeit.asc()).all()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Fahrtenübersicht: {schueler.vorname} {schueler.nachname}")

    p.setFont("Helvetica", 12)
    y = height - 90
    p.drawString(50, y, f"Adresse: {schueler.adresse}, {schueler.plz} {schueler.ort}")
    y -= 20
    p.drawString(50, y, f"Telefon: {schueler.telefon}")
    y -= 30

    if not fahrten:
        p.drawString(50, y, "Keine Fahrten protokolliert.")
    else:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Fahrten:")
        y -= 20
        p.setFont("Helvetica", 11)
        for fahrt in fahrten:
            line = f"{fahrt.datum.strftime('%d.%m.%Y')} {fahrt.uhrzeit.strftime('%H:%M')} - " \
                   f"{fahrt.typ.bezeichnung}, {fahrt.dauer_minuten} min, Bezahlt: {fahrt.bezahlt}"
            p.drawString(50, y, line)
            y -= 15

            if fahrt.inhalt:
                for note_line in fahrt.inhalt.splitlines():
                    p.drawString(60, y, f"→ {note_line}")
                    y -= 12
            y -= 5

            if y < 50:
                p.showPage()
                y = height - 50

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Fahrten_{schueler.vorname}_{schueler.nachname}.pdf'
    return response
