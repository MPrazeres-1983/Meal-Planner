from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm
from app.services.user_service import criar_utilizador, validar_login
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        utilizador = criar_utilizador(
            nome=form.nome.data, email=form.email.data, password=form.password.data
        )
        if utilizador:
            flash("Conta criada com sucesso. Já pode iniciar sessão!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Já existe uma conta com esse email.", "danger")
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utilizador = validar_login(form.email.data, form.password.data)
        if utilizador == "bloqueado":
            flash("A sua conta está bloqueada. Contacte o administrador.", "danger")
        elif utilizador:
            session["user_id"] = utilizador.id
            session["user_nome"] = utilizador.nome
            session["user_nivel"] = utilizador.nivel
            flash(f"Bem-vindo, {utilizador.nome}!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sessão terminada com sucesso.", "info")
    return redirect(url_for("auth.login"))
