from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

# Rollen: Superadmin, Fahrlehrer, Büro, Fahrschüler
class Rolle(db.Model):
    __tablename__ = 'rollen'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Rolle {self.name}>"

# Benutzer-Login (z. B. Fahrlehrer, Bürokräfte etc.)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)
    nachname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwort = db.Column(db.String(255), nullable=False)
    rolle_id = db.Column(db.Integer, db.ForeignKey('rollen.id'), nullable=False)

    rolle = db.relationship('Rolle', backref='benutzer')

# Schülerdaten (erweitert für Profilfunktion)
class Schueler(db.Model):
    __tablename__ = 'schueler'
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)
    nachname = db.Column(db.String(100), nullable=False)
    geburtsdatum = db.Column(db.Date, nullable=True)
    telefon = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    erstellt_am = db.Column(db.DateTime, default=datetime.utcnow)

    geschlecht = db.Column(db.String(10), nullable=False)  # 'männlich' oder 'weiblich'
    strasse = db.Column(db.String(150), nullable=False)
    plz = db.Column(db.String(10), nullable=False)
    ort = db.Column(db.String(100), nullable=False)
    fahrerlaubnisklasse = db.Column(db.String(20), nullable=False)
    anmeldecode = db.Column(db.String(10), unique=True, nullable=False)
    sehhilfe = db.Column(db.Boolean, default=False)
    profilbild = db.Column(db.String(255), nullable=True)
    erste_hilfe_kurs = db.Column(db.Boolean, default=False)
    sehtest = db.Column(db.Boolean, default=False)

# Definition der Fahrstundentypen
class FahrstundenTyp(db.Model):
    __tablename__ = 'fahrstundentypen'
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(100), nullable=False)
    minuten = db.Column(db.Integer, nullable=False)
    minutenpreis = db.Column(db.Numeric(5, 2), nullable=False)

    def __repr__(self):
        return f"{self.bezeichnung} ({self.minuten} Min) - {self.minutenpreis} €/Min"

# Fahrstundenprotokoll
class Fahrstundenprotokoll(db.Model):
    __tablename__ = 'fahrstundenprotokoll'
    id = db.Column(db.Integer, primary_key=True)
    schueler_id = db.Column(db.Integer, db.ForeignKey('schueler.id'), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    uhrzeit = db.Column(db.Time, nullable=False)
    dauer_minuten = db.Column(db.Integer, nullable=False)
    inhalt = db.Column(db.String(255), nullable=False)
    bezahlt = db.Column(db.String(20), nullable=False)  # z.B. 'bar', 'EC', 'Guthaben'
    fahrlehrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    typ_id = db.Column(db.Integer, db.ForeignKey('fahrstundentypen.id'), nullable=False)

    schueler = db.relationship('Schueler', backref='fahrten')
    fahrlehrer = db.relationship('User', backref='durchgefuehrte_fahrten')
    typ = db.relationship('FahrstundenTyp', backref='protokolle')

# Erweiterung für das Kassenbuch
class KassenbuchEintrag(db.Model):
    __tablename__ = 'kassenbuch'
    id = db.Column(db.Integer, primary_key=True)
    fahrstunde_id = db.Column(db.Integer, db.ForeignKey('fahrstundenprotokoll.id'), nullable=False)
    datum = db.Column(db.Date, nullable=False)
    fahrlehrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schueler_id = db.Column(db.Integer, db.ForeignKey('schueler.id'), nullable=False)
    typ = db.Column(db.String(100), nullable=False)  # z. B. "Übungsstunde", "Nachtfahrt"
    dauer_min = db.Column(db.Integer, nullable=False)
    betrag = db.Column(db.Float, nullable=False)
    zahlungsart = db.Column(db.String(20), nullable=False)  # z. B. 'bar', 'EC', 'Guthaben'

    fahrlehrer = db.relationship('User')
    schueler = db.relationship('Schueler')
    fahrstunde = db.relationship('Fahrstundenprotokoll')

class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date, nullable=False)
    uhrzeit = db.Column(db.Time, nullable=False)
    fahrlehrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schueler_id = db.Column(db.Integer, db.ForeignKey('schueler.id'), nullable=True)
    simulator = db.Column(db.Boolean, default=False)
    vergeben = db.Column(db.Boolean, default=False)
    bestätigt = db.Column(db.Boolean, default=False)

    fahrlehrer = db.relationship('User', backref='slots')
    schueler = db.relationship('Schueler', backref='slots')
