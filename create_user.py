from app import app
from models import db, User

with app.app_context():
    user = User(username="admin", password="admin123")
    db.session.add(user)
    db.session.commit()
    print("✅ User 'admin' created with password 'admin123'")
