from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Rollen: Superadmin, Fahrlehrer, Büro, Fahrschüler
class Rolle(db.Model):
    __tablename__ = 'rollen'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Rolle {self.name}>"

# Benutzer-Login (z. B. für Fahrlehrer, Bürokräfte etc.)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)
    nachname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort = db.Column(db.String(255), nullable=False)
    rolle_id = db.Column(db.Integer, db.ForeignKey('rollen.id'), nullable=False)
    rolle = db.relationship('Rolle', backref='benutzer')

# Schülerdaten (vereinfachte Stammdaten)
class Schueler(db.Model):
    __tablename__ = 'schueler'
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)
    nachname = db.Column(db.String(100), nullable=False)
    geburtsdatum = db.Column(db.Date, nullable=True)
    telefon = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    erstellt_am = db.Column(db.DateTime, default=datetime.utcnow)

# Fahrstundenprotokoll
class Fahrstundenprotokoll(db.Model):
    __tablename__ = 'fahrstundenprotokoll'
    id = db.Column(db.Integer, primary_key=True)
    schueler_id = db.Column(db.Integer, db.ForeignKey('schueler.id'), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    uhrzeit = db.Column(db.Time, nullable=False)
    dauer_minuten = db.Column(db.Integer, nullable=False)
    inhalt = db.Column(db.String(255), nullable=False)
    bezahlt = db.Column(db.String(20), nullable=False)  # z. B. 'bar', 'EC', 'Guthaben'
    fahrlehrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    schueler = db.relationship('Schueler', backref='fahrten')
    fahrlehrer = db.relationship('User', backref='durchgefuehrte_fahrten')

# models.py (Erweiterung)

class FahrstundenTyp(db.Model):
    __tablename__ = 'fahrstundentypen'
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(100), nullable=False)
    minuten = db.Column(db.Integer, nullable=False)
    minutenpreis = db.Column(db.Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f"{self.bezeichnung} ({self.minuten} Min) - {self.minutenpreis} €/Min"

# Beispielhafte Beziehung in Fahrstundenprotokoll (ergänzen):
# typ_id = db.Column(db.Integer, db.ForeignKey('fahrstundentypen.id'))
# typ = db.relationship('FahrstundenTyp', backref='protokolle')

