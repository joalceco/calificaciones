from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Sign In")


class RegisterForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    password_confirm=PasswordField("Confirma el password", validators=[DataRequired()])
    submit=SubmitField("Register")

class CursoForm(FlaskForm):
    name = StringField("Name of course", validators=[DataRequired()])
    submit=SubmitField("Register course")