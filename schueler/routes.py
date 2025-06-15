from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, make_response
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Schueler, Fahrstundenprotokoll, FahrstundenTyp
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

schueler_bp = Blueprint('schueler_bp', __name__, url_prefix='/schueler')

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

@schueler_bp.route('/profil/<int:id>')
@login_required
def schueler_profil(id):
    schueler_obj = Schueler.query.get_or_404(id)
    fahrten = Fahrstundenprotokoll.query.filter_by(schueler_id=id).order_by(
        Fahrstundenprotokoll.datum.asc(),
        Fahrstundenprotokoll.uhrzeit.asc()
    ).all()

    naechste_fahrt = Fahrstundenprotokoll.query.filter_by(schueler_id=id).filter(
        Fahrstundenprotokoll.datum >= datetime.utcnow().date()
    ).order_by(
        Fahrstundenprotokoll.datum.asc(),
        Fahrstundenprotokoll.uhrzeit.asc()
    ).first()

    return render_template('schueler/profil.html', schueler=schueler_obj, fahrten=fahrten, naechste_fahrt=naechste_fahrt)
