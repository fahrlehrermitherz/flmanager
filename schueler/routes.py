# schueler/routes.py
from flask import Blueprint, render_template
from models import db, Schueler

schueler_bp = Blueprint('schueler', __name__, url_prefix="/schueler")

@schueler_bp.route("/")
def schueler_liste():
    alle_schueler = Schueler.query.order_by(Schueler.nachname).all()
    return render_template("schueler/schueler_liste.html", schueler=alle_schueler)
