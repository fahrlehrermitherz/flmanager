from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Slot, User
from datetime import datetime

buero = Blueprint('buero', __name__, url_prefix='/buero')

# ✅ Slot-Liste
@buero.route('/slots')
@login_required
def slots_liste():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slots = Slot.query.join(User).order_by(Slot.datum.desc(), Slot.uhrzeit).all()
    return render_template('buero/slots_liste.html', slots=slots)

# ✅ Neuen Slot anlegen
@buero.route('/slots/neu', methods=['GET', 'POST'])
@login_required
def slots_neu():
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    fahrlehrer = User.query.filter(User.rolle.has(name='Fahrlehrer')).all()

    if request.method == 'POST':
        datum_str = request.form.get('datum')
        uhrzeit_str = request.form.get('uhrzeit')
        fahrlehrer_id = request.form.get('fahrlehrer_id', type=int)
        simulator = 'simulator' in request.form

        try:
            datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
            uhrzeit = datetime.strptime(uhrzeit_str, '%H:%M').time()
            neuer_slot = Slot(
                datum=datum,
                uhrzeit=uhrzeit,
                fahrlehrer_id=fahrlehrer_id,
                simulator=simulator
            )
            db.session.add(neuer_slot)
            db.session.commit()
            flash('Neuer Slot wurde erstellt.', 'success')
            return redirect(url_for('buero.slots_liste'))
        except Exception as e:
            flash(f'Fehler beim Anlegen: {e}', 'danger')

    return render_template('buero/slots_form.html', fahrlehrer=fahrlehrer, mode='neu')

# ✅ Slot bearbeiten
@buero.route('/slots/edit/<int:slot_id>', methods=['GET', 'POST'])
@login_required
def slots_edit(slot_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slot = Slot.query.get_or_404(slot_id)
    fahrlehrer = User.query.filter(User.rolle.has(name='Fahrlehrer')).all()

    if request.method == 'POST':
        slot.datum = datetime.strptime(request.form.get('datum'), '%Y-%m-%d').date()
        slot.uhrzeit = datetime.strptime(request.form.get('uhrzeit'), '%H:%M').time()
        slot.fahrlehrer_id = request.form.get('fahrlehrer_id', type=int)
        slot.simulator = 'simulator' in request.form

        db.session.commit()
        flash('Slot wurde aktualisiert.', 'success')
        return redirect(url_for('buero.slots_liste'))

    return render_template('buero/slots_form.html', fahrlehrer=fahrlehrer, slot=slot, mode='edit')

# ✅ Slot löschen
@buero.route('/slots/delete/<int:slot_id>', methods=['POST'])
@login_required
def slots_delete(slot_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slot = Slot.query.get_or_404(slot_id)
    db.session.delete(slot)
    db.session.commit()
    flash('Slot wurde gelöscht.', 'info')
    return redirect(url_for('buero.slots_liste'))

# ✅ Slot bestätigen
@buero.route('/slots/confirm/<int:slot_id>', methods=['POST'])
@login_required
def slots_confirm(slot_id):
    if current_user.rolle.name not in ['Büro', 'Superadmin']:
        return "Nicht autorisiert", 403

    slot = Slot.query.get_or_404(slot_id)
    slot.bestätigt = True
    db.session.commit()
    flash('Slot wurde bestätigt.', 'success')
    return redirect(url_for('buero.slots_liste'))
