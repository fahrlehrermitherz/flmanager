from flask import Blueprint, render_template, request
from datetime import datetime
from models import db, Fahrstundenprotokoll, User, Schueler
from flask_login import login_required, current_user

buero = Blueprint('buero', __name__, url_prefix='/buero')

@buero.route('/kassenbuch')
@login_required
def kassenbuch():
    if current_user.rolle.name != 'Büro':
        return "Nicht autorisiert", 403

    monat_filter = request.args.get('monat')
    query = Fahrstundenprotokoll.query.join(User).join(Schueler)

    if monat_filter:
        try:
            jahr, monat = map(int, monat_filter.split("-"))
            start_datum = datetime(jahr, monat, 1)
            if monat == 12:
                end_datum = datetime(jahr + 1, 1, 1)
            else:
                end_datum = datetime(jahr, monat + 1, 1)
            query = query.filter(Fahrstundenprotokoll.datum >= start_datum,
                                 Fahrstundenprotokoll.datum < end_datum)
        except:
            pass

    fahrten = query.order_by(Fahrstundenprotokoll.datum.desc()).all()

    # Typenlogik simulieren (kann später ersetzt werden durch Typ-Tabelle)
    def get_typ(dauer, inhalt):
        if "Nacht" in inhalt:
            return "Nachtfahrt", 1.2
        elif "Autobahn" in inhalt:
            return "Autobahnfahrt", 1.1
        elif "Überland" in inhalt:
            return "Überlandfahrt", 1.0
        elif "Schalt" in inhalt:
            return "Schaltkompetenz", 1.0
        else:
            return "Übungsfahrt", 1.0  # Standardwert

    kassenbuch = []
    minutenpreis = 1.00  # TODO: Dynamisch machen, z. B. aus DB

    for fahrt in fahrten:
        typ_name, multiplikator = get_typ(fahrt.dauer_minuten, fahrt.inhalt)
        eintrag = {
            "datum": fahrt.datum,
            "fahrlehrer": fahrt.fahrlehrer,
            "schueler": fahrt.schueler,
            "typ": typ_name,
            "dauer_minuten": fahrt.dauer_minuten,
            "zahlungsart": fahrt.bezahlt,
            "betrag": fahrt.dauer_minuten * minutenpreis * multiplikator
        }
        kassenbuch.append(eintrag)

    return render_template("buero/kassenbuch.html", kassenbuch=kassenbuch)
