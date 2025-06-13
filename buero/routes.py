from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, FahrstundenTyp

buero = Blueprint('buero', __name__, url_prefix='/buero')

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
