CREATE TABLE IF NOT EXISTS rollen (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    passwort VARCHAR(255) NOT NULL,
    rolle_id INTEGER NOT NULL REFERENCES rollen(id)
);

CREATE TABLE IF NOT EXISTS schueler (
    id SERIAL PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE,
    telefon VARCHAR(50),
    email VARCHAR(120),
    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    geschlecht VARCHAR(10) NOT NULL,
    strasse VARCHAR(150) NOT NULL,
    plz VARCHAR(10) NOT NULL,
    ort VARCHAR(100) NOT NULL,
    fahrerlaubnisklasse VARCHAR(20) NOT NULL,
    anmeldecode VARCHAR(10) UNIQUE NOT NULL,
    sehhilfe BOOLEAN DEFAULT FALSE,
    profilbild VARCHAR(255),
    erste_hilfe_kurs BOOLEAN DEFAULT FALSE,
    sehtest BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS fahrstundentypen (
    id SERIAL PRIMARY KEY,
    bezeichnung VARCHAR(100) NOT NULL,
    minuten INTEGER NOT NULL,
    minutenpreis NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS fahrstundenprotokoll (
    id SERIAL PRIMARY KEY,
    schueler_id INTEGER NOT NULL REFERENCES schueler(id),
    datum DATE NOT NULL,
    uhrzeit TIME NOT NULL,
    dauer_minuten INTEGER NOT NULL,
    inhalt VARCHAR(255) NOT NULL,
    bezahlt VARCHAR(20) NOT NULL,
    fahrlehrer_id INTEGER NOT NULL REFERENCES users(id),
    typ_id INTEGER NOT NULL REFERENCES fahrstundentypen(id)
);

CREATE TABLE IF NOT EXISTS kassenbuch (
    id SERIAL PRIMARY KEY,
    fahrstunde_id INTEGER NOT NULL REFERENCES fahrstundenprotokoll(id),
    datum DATE NOT NULL,
    fahrlehrer_id INTEGER NOT NULL REFERENCES users(id),
    schueler_id INTEGER NOT NULL REFERENCES schueler(id),
    typ VARCHAR(100) NOT NULL,
    dauer_min INTEGER NOT NULL,
    betrag FLOAT NOT NULL,
    zahlungsart VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS slots (
    id SERIAL PRIMARY KEY,
    datum DATE NOT NULL,
    uhrzeit TIME NOT NULL,
    fahrlehrer_id INTEGER NOT NULL REFERENCES users(id),
    schueler_id INTEGER REFERENCES schueler(id),
    simulator BOOLEAN DEFAULT FALSE,
    vergeben BOOLEAN DEFAULT FALSE,
    bestaetigt BOOLEAN DEFAULT FALSE
);
