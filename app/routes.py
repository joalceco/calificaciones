from app import app
from flask import render_template, url_for, redirect, request, flash
from app.forms import LoginForm, RegisterForm, CursoForm, TareaForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Curso, Tarea, Calificaciones
from app import db

@app.route("/")
@login_required
def index():
    if current_user.admin or current_user.profesor:
        return render_template("index.html")
    else:
        return redirect(url_for("cursos_index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None or not user.check_password(form.password.data):
            flash("Correo o contraseña no validos")
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
            # TODO: flash "ya estas reguistrado"-
            return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# cursos
@app.route("/cursos", methods=["GET"])
@login_required
def cursos_index():
    #TODO: añadir filtro para que solo puedan acceder profesores
    cursos = Curso.query.filter_by(id_profesor=current_user.id).all()
    # print(current_user.cursos_de_alumno)
    return render_template("cursos_index.html",cursos = cursos)


@app.route("/cursos/<int:id>")
@login_required
def cursos_show(id):
    curso = Curso.query.filter_by(id=id).first()
    
    return render_template("cursos_show.html", curso=curso)

@app.route("/cursos/create", methods=["GET", "POST"])
def cursos_create():
    form=CursoForm()
    if form.validate_on_submit():
        curso = Curso(name=form.name.data, id_profesor=current_user.id)
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos_index"))
    else:
        #pidiento el formulario
        return render_template("curso_create.html", form=form)


# <!-- cursos/<id>/alumnos/storecursos_alumnos_store-->
@app.route("/cursos/<int:id_curso>/alumnos/store" , methods=["POST"])
@login_required
def cursos_alumnos_store(id_curso):
    correos = request.form["alumnos"]
    correos = correos.replace(" ", "")
    correos = correos.split(",")
    sadas = ""
    curso = Curso.query.filter_by(id=id_curso).first()
    for correo in correos: 
        # Si el alumno ya esta inscrito saltar
        alumno = User.query.filter_by(email=correo).first()
        if alumno:
            # if alumno ya inscrito no instcribir
            curso.alumnos.append(alumno)
        else:
            #TODO: Flash con alumno no encontrado
            pass
    db.session.add(curso)
    db.session.commit()
    return redirect(url_for("cursos_show", id=id_curso))

@app.route("/cursos/destroy/<int:id>")
@login_required
def cursos_destroy(id):
    # Revisar la bd si existe ese curso con ese id
    curso = Curso.query.filter_by(id=id).first()
    if curso and curso.id_profesor == current_user.id:
        db.session.delete(curso)
        db.session.commit()
    else:
        flash("No tienes permisos para eliminar este recurso")
    # Redireccionar a cursos create
    return redirect(url_for("cursos_index"))
    # return str(curso.name)


# Tareas

@app.route("/cursos/<int:id>/tareas/create",  methods=["GET", "POST"])
@login_required
def cursos_tareas_create(id):
    curso = Curso.query.filter_by(id=id).first()
    form = TareaForm()
    if form.validate_on_submit():
        # Post
        tarea = Tarea()
        tarea.titulo = form.titulo.data
        tarea.id_curso = id
        tarea.fecha_de_creacion = form.fecha_de_creacion.data
        tarea.fecha_de_entrega = form.fecha_de_entrega.data
        tarea.descripcion= form.descripcion.data
        tarea.puntaje = form.puntos.data
        db.session.add(tarea)
        db.session.commit()
        return redirect(url_for("cursos_tareas_index", id=id)) # TODO: Cambiar
    else:
        return render_template("cursos_tareas_create.html", curso=curso, form=form)


@app.route("/cursos/<int:id>/tareas",  methods=["GET", "POST"])
@login_required
def cursos_tareas_index(id):
    curso = Curso.query.filter_by(id=id).first()
    tareas = Tarea.query.filter_by(id_curso=id).all()
    for tarea in tareas:
        print(tarea.calificaciones.calificacion)
    return render_template("cursos_tareas_index.html", curso=curso, tareas=tareas)


# Calificaicones

@app.route("/cursos/<int:id>/tareas/calificaciones",  methods=["GET"])
@login_required
def cursos_tareas_calificaciones_index(id_curso):
    curso = Curso.query.filter_by(id=id_curso).first()
    calificaciones = Calificaciones.query.filter_by(id_tarea=id_tarea).all()
    calificaciones_dict={}
    for calificacion in calificaciones:
        calificaciones_dict[calificacion.id_alumno] = calificacion.calificacion
    print(calificaciones_dict)
    return render_template("cursos_tareas_calificaciones_edit.html", 
                            curso=curso, 
                            tarea=tarea, 
                            alumnos=curso.alumnos, 
                            calificaciones=calificaciones_dict)

# cursos_tareas_calificaciones_edit', id_curso=curso.id, id_tarea=tarea.id
@app.route("/cursos/<int:id_curso>/tareas/<int:id_tarea>/edit",  methods=["GET"])
@login_required
def cursos_tareas_calificaciones_edit(id_curso, id_tarea):
    curso = Curso.query.filter_by(id=id_curso).first()
    tarea = Tarea.query.filter_by(id=id_tarea).first()
    calificaciones = Calificaciones.query.filter_by(id_tarea=id_tarea).all()
    calificaciones_dict={}
    for calificacion in calificaciones:
        calificaciones_dict[calificacion.id_alumno] = calificacion.calificacion
    print(calificaciones_dict)
    return render_template("cursos_tareas_calificaciones_edit.html", 
                            curso=curso, 
                            tarea=tarea, 
                            alumnos=curso.alumnos, 
                            calificaciones=calificaciones_dict)

@app.route("/cursos/<int:id_curso>/tareas/<int:id_tarea>/update",  methods=["POST"])
@login_required
def cursos_tareas_calificaciones_update(id_curso, id_tarea):
    calificaciones = request.form
    for id_alumno,calificaion_tarea in calificaciones.items():
        # print(id_alumno,value)
        calificacion = Calificaciones.query.filter_by(id_alumno=id_alumno, id_tarea=id_tarea).first()
        if not calificacion:
            calificacion = Calificaciones()
            calificacion.id_alumno=id_alumno
            calificacion.id_tarea = id_tarea
        calificacion.calificacion = calificaion_tarea
        
        db.session.add(calificacion)
    db.session.commit()
    return redirect(url_for("cursos_tareas_calificaciones_edit", id_tarea=id_tarea, id_curso=id_curso))