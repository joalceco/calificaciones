from app import app
from flask import render_template, url_for, redirect
from app.forms import LoginForm

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        # Lidear con datos de login
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)
    