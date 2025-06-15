from flmanager import create_app, db  # yourappname ersetzen!
# Beispiel: from app import create_app, db wenn dein Ordner "app" heißt

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tabellen wurden erstellt.")
