from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Schueler, Fahrstundenprotokoll, FahrstundenTyp, User

schueler_bp = Blueprint('schueler', __name__)


@schueler_bp.route('/fahrstunde/anlegen', methods=['GET', 'POST'])
@login_required
def fahrstunde_anlegen():
    if request.method == 'POST':
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

        return redirect(url_for('schueler.fahrstunde_anlegen'))

    schueler = Schueler.query.all()
    typen = FahrstundenTyp.query.all()

    return render_template('schueler/fahrstunde_anlegen.html', schueler=schueler, typen=typen)

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
