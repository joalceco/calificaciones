from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(120))
    apellido_paterno = db.Column(db.String(120), index=True)
    apellido_materno = db.Column(db.String(120))
    matricula=db.Column(db.String(10), index=True, unique=True)
    password_hash=db.Column(db.String(128))
    cursos=db.relationship("Curso", backref="profesor", lazy="dynamic")

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "Usuario: {}, email: {}".format(self.matricula, self.email)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    id_profesor = db.Column(db.Integer, db.ForeignKey("user.id"))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))