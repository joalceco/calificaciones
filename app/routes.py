from app import app
from flask import render_template, url_for, redirect
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user
from app.models import User

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
            login_user(user, rememeber=form.remember_me.data)
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
        if user is None and form.password.data==form.password_check.data:
            user = User(email=email)
            user.set_password(form.password.data)
            db.add(user)
            db.commit()
            login_user(user, rememeber=True)
            return redirect(url_for("login"))
        else:
            # TODO: flash "ya estas reguistrado"
            return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)