from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.recipe import Recipe
from app.forms.category_form import CategoriaForm
from app.forms.recipe_form import RecipeForm
from app.forms.auxiliares import FormApagarCategoria
from app.services.category_service import listar_categorias
from app.services.recipe_service import (
    listar_pendentes,
    aprovar_receita,
    eliminar_receita,
)
from app.services.category_service import (
    listar_categorias,
    criar_categoria,
    eliminar_categoria,
    editar_categoria,
    obter_categoria_por_id,
)
from app.services.user_service import (
    obter_utilizador_por_id,
    listar_todos_utilizadores,
    atualizar_dados_utilizador,
    eliminar_utilizador,
    alternar_estado_utilizador,
)
from app.forms.user_admin_form import EditarUserForm, ConfirmarAcaoForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def exigir_administrador():
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))



@admin_bp.route("/aprovar_receitas")
def aprovar_receitas():
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    pendentes = listar_pendentes()
    return render_template("admin/aprovar_receitas.html", pendentes=pendentes)


@admin_bp.route("/aprovar_receita/<int:receita_id>", methods=["POST"])
def aprovar_receita_admin(receita_id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    receita = aprovar_receita(receita_id)
    if receita:
        flash("Receita aprovada com sucesso.", "success")
    else:
        flash("Erro ao aprovar a receita.", "danger")

    return redirect(url_for("admin.aprovar_receitas"))


@admin_bp.route("/recusar_receita/<int:receita_id>", methods=["POST"])
def recusar_receita_admin(receita_id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    if eliminar_receita(receita_id):
        flash("Receita recusada (eliminada) com sucesso.", "warning")
    else:
        flash("Erro ao recusar a receita.", "danger")

    return redirect(url_for("admin.aprovar_receitas"))


@admin_bp.route("/categorias")
def gerir_categorias():
    if not session.get("user_nivel") == 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    categorias = listar_categorias()
    return render_template(
        "admin/categorias.html",
        categorias=categorias,
        form_apagar=FormApagarCategoria(),
    )


@admin_bp.route("/categorias/criar", methods=["GET", "POST"])
def criar_categoria_admin():
    form = CategoriaForm()
    if form.validate_on_submit():
        nova = criar_categoria(form.nome.data)
        if nova:
            flash("Categoria criada com sucesso!", "success")
        else:
            flash("Já existe uma categoria com esse nome ou nome inválido.", "warning")
        return redirect(url_for("admin.gerir_categorias"))
    return render_template("admin/criar_categoria.html", form=form)


@admin_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def editar_categoria_admin(id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    categoria = obter_categoria_por_id(id)
    if not categoria:
        flash("Categoria não encontrada.", "danger")
        return redirect(url_for("admin.gerir_categorias"))

    form = CategoriaForm(obj=categoria)
    form.submit.label.text = "Atualizar Categoria"  # <-- aqui

    if form.validate_on_submit():
        editar_categoria(id, form.nome.data)
        flash("Categoria atualizada com sucesso.", "success")
        return redirect(url_for("admin.gerir_categorias"))

    return render_template(
        "admin/editar_categoria.html", form=form, categoria=categoria
    )


@admin_bp.route("/categorias/apagar/<int:id>", methods=["POST"])
def eliminar_categoria_admin(id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    if eliminar_categoria(id):
        flash("Categoria eliminada com sucesso.", "success")
    else:
        flash(
            "Não foi possível eliminar a categoria. Encontra-se associada a pelo menos uma receita",
            "danger",
        )
    return redirect(url_for("admin.gerir_categorias"))


@admin_bp.route("/utilizadores")
def listar_utilizadores():
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    utilizadores = listar_todos_utilizadores()
    form_apagar = ConfirmarAcaoForm()
    return render_template(
        "admin/utilizadores.html", utilizadores=utilizadores, form_apagar=form_apagar
    )


@admin_bp.route("/utilizador/<int:id>")
def ver_utilizador(id):
    utilizador = obter_utilizador_por_id(id)
    if not utilizador:
        flash("Utilizador não encontrado.", "warning")
        return redirect(url_for("admin.listar_utilizadores"))

    return render_template("admin/ver_utilizador.html", utilizador=utilizador)


@admin_bp.route("/utilizador/<int:id>/editar", methods=["GET", "POST"])
def editar_utilizador(id):
    utilizador = obter_utilizador_por_id(id)
    if not utilizador:
        flash("Utilizador não encontrado.", "warning")
        return redirect(url_for("admin.listar_utilizadores"))

    form = EditarUserForm(obj=utilizador)
    if form.validate_on_submit():
        atualizar_dados_utilizador(
            id,
            novo_nome=form.nome.data,
            novo_email=form.email.data,
            novo_nivel=int(form.nivel.data),
        )
        flash("Utilizador atualizado com sucesso.", "success")
        return redirect(url_for("admin.ver_utilizador", id=id))

    form.nivel.data = str(utilizador.nivel)
    return render_template(
        "admin/editar_utilizador.html", form=form, utilizador=utilizador
    )


@admin_bp.route("/utilizador/<int:id>/bloquear", methods=["POST"])
def bloquear_utilizador(id):
    form = ConfirmarAcaoForm()
    if form.validate_on_submit():
        alternar_estado_utilizador(id)
        flash("Estado de conta atualizado com sucesso.", "info")
    else:
        flash("Ação inválida.", "danger")
    return redirect(url_for("admin.listar_utilizadores"))


@admin_bp.route("/utilizador/<int:id>/apagar", methods=["POST"])
def apagar_utilizador(id):
    form = ConfirmarAcaoForm()
    if form.validate_on_submit():
        eliminar_utilizador(id)
        flash("Utilizador eliminado com sucesso.", "warning")
    else:
        flash("Ação inválida.", "danger")
    return redirect(url_for("admin.listar_utilizadores"))


@admin_bp.route("/receitas")
def listar_receitas():
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Recipe.query

    if search:
        query = query.filter(Recipe.titulo.ilike(f"%{search}%"))

    pagination = query.order_by(Recipe.data_submetida.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template(
        "admin/listar_receitas.html", receitas=pagination.items, pagination=pagination
    )


@admin_bp.route("/receitas/<int:receita_id>/apagar", methods=["POST"])
def apagar_receita(receita_id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    sucesso, mensagem = eliminar_receita(receita_id)
    if sucesso:
        flash("Receita eliminada com sucesso.", "success")
    else:
        flash(mensagem or "Erro ao eliminar a receita.", "danger")

    return redirect(request.referrer or url_for("admin.listar_receitas"))


@admin_bp.route("/receitas/<int:receita_id>/editar", methods=["GET", "POST"])
def editar_receita(receita_id):
    if session.get("user_nivel") != 3:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("main.home"))

    receita = Recipe.query.get_or_404(receita_id)
    form = RecipeForm(obj=receita)

    # Preencher as opções de categoria
    categorias = listar_categorias()
    form.categoria_id.choices = [(c.id, c.nome) for c in categorias]

    if form.validate_on_submit():
        form.populate_obj(receita)

        # Verificar se a receita deve ser aprovada
        aprovar = request.form.get("aprovar") == "on"
        receita.aprovada = aprovar

        # Se a receita for aprovada, podemos definir publicada com base na escolha do usuário
        if receita.aprovada:
            receita.publicada = form.publica.data

        from app.db import db

        db.session.commit()

        flash("Receita atualizada com sucesso.", "success")
        return redirect(url_for("admin.listar_receitas"))

    # Preencher o campo publica com o valor atual
    form.publica.data = receita.publicada

    return render_template("admin/editar_receita.html", form=form, receita=receita)
