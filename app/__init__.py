from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
# if app.config.get('ADMIN_PASS'):
#     from app.models import User 
#     if not User.query.filter_by(email="admin@admin.com").first():
#         u = User()
#         u.create_admin(app.config.get('ADMIN_PASS'))
#         db.session.add(u)
#         db.session.commit()

from app import routes, models