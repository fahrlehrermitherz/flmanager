from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, FahrstundenTyp, Fahrstundenprotokoll, User, Schueler, Rolle

buero = Blueprint('buero', __name__, url_prefix='/buero')

# 📊 Büro-Dashboard
@buero.route('/dashboard')
@login_required
def dashboard():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    anzahl_fahrten = Fahrstundenprotokoll.query.count()
    anzahl_typen = FahrstundenTyp.query.count()

    fahrlehrer_rolle = Rolle.query.filter_by(name='Fahrlehrer').first()
    anzahl_fahrlehrer = (
        User.query.filter_by(rolle=fahrlehrer_rolle).count() if fahrlehrer_rolle else 0
    )
    anzahl_schueler = Schueler.query.count()

    return render_template(
        'buero/dashboard.html',
        anzahl_fahrten=anzahl_fahrten,
        anzahl_typen=anzahl_typen,
        anzahl_fahrlehrer=anzahl_fahrlehrer,
        anzahl_schueler=anzahl_schueler
    )

# 💶 Fahrstunden-Typen Übersicht
@buero.route('/preise')
@login_required
def preise():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    typen = FahrstundenTyp.query.order_by(FahrstundenTyp.bezeichnung.asc()).all()
    return render_template('buero/preise.html', typen=typen)

# 💡 Neuen Typ anlegen
@buero.route('/preise/neu', methods=['GET', 'POST'])
@login_required
def preise_neu():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    if request.method == 'POST':
        bezeichnung = request.form.get('bezeichnung', '').strip()
        minuten = request.form.get('minuten', type=int)
        minutenpreis = request.form.get('minutenpreis', type=float)

        if not bezeichnung or not minuten or minuten <= 0 or not minutenpreis or minutenpreis < 0:
            flash('Bitte alle Felder korrekt ausfüllen.', 'danger')
        else:
            neuer_typ = FahrstundenTyp(
                bezeichnung=bezeichnung,
                minuten=minuten,
                minutenpreis=minutenpreis
            )
            db.session.add(neuer_typ)
            db.session.commit()
            flash('Neuer Fahrstunden-Typ wurde gespeichert.', 'success')
            return redirect(url_for('buero.preise'))

    return render_template('buero/preise_neu.html')

# 📝 Typ bearbeiten
@buero.route('/preise/edit/<int:typ_id>', methods=['GET', 'POST'])
@login_required
def preise_edit(typ_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    typ = FahrstundenTyp.query.get_or_404(typ_id)

    if request.method == 'POST':
        typ.bezeichnung = request.form.get('bezeichnung', '').strip()
        typ.minuten = request.form.get('minuten', type=int)
        typ.minutenpreis = request.form.get('minutenpreis', type=float)

        if not typ.bezeichnung or not typ.minuten or typ.minuten <= 0 or not typ.minutenpreis or typ.minutenpreis < 0:
            flash('Bitte alle Felder korrekt ausfüllen.', 'danger')
        else:
            db.session.commit()
            flash('Fahrstunden-Typ wurde aktualisiert.', 'success')
            return redirect(url_for('buero.preise'))

    return render_template('buero/preise_edit.html', typ=typ)

# ❌ Typ löschen
@buero.route('/preise/delete/<int:typ_id>', methods=['POST'])
@login_required
def preise_delete(typ_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    typ = FahrstundenTyp.query.get_or_404(typ_id)
    db.session.delete(typ)
    db.session.commit()
    flash('Fahrstunden-Typ wurde gelöscht.', 'info')
    return redirect(url_for('buero.preise'))
