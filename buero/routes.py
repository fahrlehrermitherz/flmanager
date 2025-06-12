from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, User, Fahrstundenprotokoll, Rolle
from sqlalchemy import extract

buero = Blueprint("buero", __name__, url_prefix="/buero")

@buero.route("/verwaltung")
@login_required
def verwaltung():
    if current_user.rolle.name != "Büro":
        return "Zugriff verweigert", 403

    monat = request.args.get("monat")
    jahr = request.args.get("jahr")

    query = Fahrstundenprotokoll.query.join(User, Fahrstundenprotokoll.fahrlehrer).order_by(
        Fahrstundenprotokoll.datum.desc()
    )

    if monat and jahr:
        query = query.filter(
            extract("month", Fahrstundenprotokoll.datum) == int(monat),
            extract("year", Fahrstundenprotokoll.datum) == int(jahr)
        )

    fahrten = query.all()

    # Fahrlehrer-Preise (dynamisch später aus Datenbank holen)
    minutenpreise = {
        "default": 1.20  # Fallback-Preis pro Minute
    }

    return render_template("buero/verwaltungsseite.html", fahrten=fahrten, minutenpreise=minutenpreise)
