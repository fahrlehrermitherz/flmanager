from flask import Blueprint, render_template, session, redirect, url_for
from models import Schueler
from datetime import date

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    anzahl_schueler = Schueler.query.count()
    heute = date.today().strftime("%d.%m.%Y")

    return render_template("main/dashboard.html", anzahl_schueler=anzahl_schueler, heute=heute)
