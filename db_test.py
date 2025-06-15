from sqlalchemy import create_engine

# Railway interne URL, wenn du das direkt im Container laufen lässt
DB_URL = "postgresql://postgres:bydexzqxToeTpGxCynAynqxRRqBThlXd@postgres.railway.internal:5432/railway"

# Wenn du lokal testen willst (DbGate etc.)
# DB_URL = "postgresql://postgres:bydexzqxToeTpGxCynAynqxRRqBThlXd@nozomi.proxy.rlwy.net:37182/railway"

engine = create_engine(DB_URL)

try:
    with engine.connect() as connection:
        print("✅ Verbindung erfolgreich!")
except Exception as e:
    print("❌ Verbindungsfehler:", e)
