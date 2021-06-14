from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email=StringField("Correo electronico", validators=[DataRequired(), Email()])
    password=PasswordField("Contraseña", validators=[DataRequired()])
    remember_me=BooleanField("Recuerdame")
    submit=SubmitField("Iniciar Sesión")


class RegisterForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    password_confirm=PasswordField("Confirma el password", validators=[DataRequired()])
    submit=SubmitField("Register")

class CursoForm(FlaskForm):
    name = StringField("Name of course", validators=[DataRequired()])
    submit=SubmitField("Register course")

class TareaForm(FlaskForm):
    titulo = StringField("Titulo", validators=[DataRequired()])
    fecha_de_creacion = DateTimeField("Fecha de creación",format='%d-%m-%Y %H:%M:%S')
    fecha_de_entrega = DateTimeField("Fecha de entrega", format='%d-%m-%Y %H:%M:%S')
    descripcion = StringField("Descripción")
    puntos = IntegerField("Puntos")
    submit=SubmitField("Registrar Tarea")