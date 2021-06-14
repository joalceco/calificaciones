import click
from app import app
from app.models import User
from app import db

@app.cli.command("create-admin")
def create_admin():
    if not User.query.filter_by(email="admin@admin.com").first():
        u = User()
        u.create_admin(app.config.get('ADMIN_PASS'))
        db.session.add(u)
        db.session.commit()