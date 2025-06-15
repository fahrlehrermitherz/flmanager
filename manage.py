from app import create_app, db
from models import *

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Datenbanktabellen wurden beim Start erstellt.")

if __name__ == "__main__":
    app.run()
