from app import app
from flask import render_template, url_for, redirect
from app.forms import LoginForm, RegisterForm, CursoForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Curso
from app import db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])

def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None or not user.check_password(form.password.data):
            print("No estoy en la base datos o no es la contraseña")
            # TODO: flash con el error.
            return redirect(url_for("login"))
        else:
            login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None and form.password.data==form.password_confirm.data:
            user = User(email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("login"))
        else:
            # TODO: flash "ya estas reguistrado"
            return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# cursos
@app.route("/cursos", methods=["GET"])
def cursos_index():
    return "Aqui vemos los cursos"

@app.route("/cursos/create", methods=["GET", "POST"])
def cursos_create():
    form=CursoForm()
    if form.validate_on_submit():
        curso = Curso(name=form.name.data, id_profesor=current_user.id)
        db.session.add(curso)
        db.session.commit()
        return "Entro"
        
    else:
        #pidiento el formulario
        return render_template("curso_create.html", form=form)