from flask import Blueprint, render_template, request
from datetime import datetime
from models import db, Fahrstundenprotokoll, User, Schueler
from flask_login import login_required, current_user

buero = Blueprint('buero', __name__, url_prefix='/buero')

@buero.route('/kassenbuch')
@login_required
def kassenbuch():
    # Nur Büro oder Superadmin erlaubt
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    monat_filter = request.args.get('monat')
    query = Fahrstundenprotokoll.query.join(User).join(Schueler)

    if monat_filter:
        try:
            jahr, monat = map(int, monat_filter.split("-"))
            start_datum = datetime(jahr, monat, 1)
            end_datum = datetime(jahr + (monat // 12), (monat % 12) + 1, 1)
            query = query.filter(
                Fahrstundenprotokoll.datum >= start_datum,
                Fahrstundenprotokoll.datum < end_datum
            )
        except ValueError:
            pass  # Ungültiger Filter? Kein Crash – einfach alles zeigen.

    fahrten = query.order_by(Fahrstundenprotokoll.datum.desc()).all()

    # 🔄 Typenlogik zentral auslagern – später evtl. DB-Tabelle „Fahrstundentypen“
    def get_typ(dauer, inhalt):
        inhalt_lower = inhalt.lower()
        if "nacht" in inhalt_lower:
            return "Nachtfahrt", 1.2
        elif "autobahn" in inhalt_lower:
            return "Autobahnfahrt", 1.1
        elif "überland" in inhalt_lower:
            return "Überlandfahrt", 1.0
        elif "schalt" in inhalt_lower:
            return "Schaltkompetenz", 1.0
        else:
            return "Übungsfahrt", 1.0

    # 🔢 Preisbasis – später über Settings-Model steuerbar machen
    minutenpreis_basis = 1.00

    kassenbuch = []
    for fahrt in fahrten:
        typ_name, multiplikator = get_typ(fahrt.dauer_minuten, fahrt.inhalt)
        betrag = fahrt.dauer_minuten * minutenpreis_basis * multiplikator
        kassenbuch.append({
            "datum": fahrt.datum,
            "fahrlehrer": f"{fahrt.fahrlehrer.vorname} {fahrt.fahrlehrer.nachname}",
            "schueler": f"{fahrt.schueler.vorname} {fahrt.schueler.nachname}",
            "typ": typ_name,
            "dauer_minuten": fahrt.dauer_minuten,
            "zahlungsart": fahrt.bezahlt,
            "betrag": round(betrag, 2)
        })

    return render_template("buero/kassenbuch.html", kassenbuch=kassenbuch, monat_filter=monat_filter)
