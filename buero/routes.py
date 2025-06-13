from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, FahrstundenTyp, Fahrstundenprotokoll, Slot, User, Schueler, Rolle

buero = Blueprint('buero', __name__, url_prefix='/buero')

# 🚀 Dashboard
@buero.route('/dashboard')
@login_required
def dashboard():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    anzahl_fahrten = Fahrstundenprotokoll.query.count()
    anzahl_typen = FahrstundenTyp.query.count()
    fahrlehrer_rolle = Rolle.query.filter_by(name='Fahrlehrer').first()
    anzahl_fahrlehrer = User.query.filter_by(rolle=fahrlehrer_rolle).count() if fahrlehrer_rolle else 0
    anzahl_schueler = Schueler.query.count()

    return render_template('buero/dashboard.html',
                           anzahl_fahrten=anzahl_fahrten,
                           anzahl_typen=anzahl_typen,
                           anzahl_fahrlehrer=anzahl_fahrlehrer,
                           anzahl_schueler=anzahl_schueler)

# 💶 Preisverwaltung
@buero.route('/preise')
@login_required
def preise_liste():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    typen = FahrstundenTyp.query.order_by(FahrstundenTyp.bezeichnung).all()
    return render_template('buero/preise_liste.html', typen=typen)

@buero.route('/preise/neu', methods=['GET', 'POST'])
@login_required
def preise_neu():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    if request.method == 'POST':
        bezeichnung = request.form.get('bezeichnung')
        minuten = request.form.get('minuten', type=int)
        minutenpreis = request.form.get('minutenpreis', type=float)
        if not bezeichnung or not minuten or not minutenpreis:
            flash('Alle Felder müssen ausgefüllt sein.', 'danger')
        else:
            neuer_typ = FahrstundenTyp(bezeichnung=bezeichnung, minuten=minuten, minutenpreis=minutenpreis)
            db.session.add(neuer_typ)
            db.session.commit()
            flash('Fahrstunden-Typ hinzugefügt.', 'success')
            return redirect(url_for('buero.preise_liste'))
    return render_template('buero/preise_form.html', mode='neu')

@buero.route('/preise/edit/<int:typ_id>', methods=['GET', 'POST'])
@login_required
def preise_edit(typ_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    typ = FahrstundenTyp.query.get_or_404(typ_id)
    if request.method == 'POST':
        typ.bezeichnung = request.form.get('bezeichnung')
        typ.minuten = request.form.get('minuten', type=int)
        typ.minutenpreis = request.form.get('minutenpreis', type=float)
        db.session.commit()
        flash('Fahrstunden-Typ aktualisiert.', 'success')
        return redirect(url_for('buero.preise_liste'))
    return render_template('buero/preise_form.html', mode='edit', typ=typ)

@buero.route('/preise/delete/<int:typ_id>', methods=['POST'])
@login_required
def preise_delete(typ_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    typ = FahrstundenTyp.query.get_or_404(typ_id)
    db.session.delete(typ)
    db.session.commit()
    flash('Fahrstunden-Typ gelöscht.', 'info')
    return redirect(url_for('buero.preise_liste'))

# 📘 Slots Übersicht (inkl. Simulator)
@buero.route('/slots')
@login_required
def slots_uebersicht():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    slots = Slot.query.order_by(Slot.datum.desc(), Slot.uhrzeit.desc()).all()
    return render_template('buero/slots_uebersicht.html', slots=slots)

@buero.route('/slots/bestaetigen/<int:slot_id>', methods=['POST'])
@login_required
def slot_bestaetigen(slot_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    slot = Slot.query.get_or_404(slot_id)
    if slot.simulator:
        slot.bestätigt = True
        db.session.commit()
        flash('Simulator-Slot bestätigt.', 'success')
    else:
        flash('Nur Simulator-Slots dürfen hier bestätigt werden.', 'danger')
    return redirect(url_for('buero.slots_uebersicht'))

# 📒 Kassenbuch (optional: Export)
@buero.route('/kassenbuch')
@login_required
def kassenbuch():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403
    fahrten = Fahrstundenprotokoll.query.order_by(Fahrstundenprotokoll.datum.desc()).all()
    return render_template('buero/kassenbuch.html', fahrten=fahrten)
