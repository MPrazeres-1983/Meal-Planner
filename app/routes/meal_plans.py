from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
    send_file,
)
from app.forms.meal_plan_form import MealPlanForm
from app.services.meal_plan_service import (
    criar_plano_semanal,
    obter_planos_do_utilizador,
    obter_plano_completo,
    eliminar_plano,
    atualizar_plano_semanal,
    exportar_plano_para_pdf,
)
from app.services.recipe_service import listar_receitas
from io import BytesIO
from datetime import datetime, timedelta
from app.forms.auxiliares import FormApagarPlano

meal_plans_bp = Blueprint("meal_plans", __name__, url_prefix="/planos")


@meal_plans_bp.route("/criar", methods=["GET", "POST"])
def criar():
    if "user_id" not in session:
        flash("Tem de iniciar sessão para criar um plano semanal.", "warning")
        return redirect(url_for("auth.login"))

    form = MealPlanForm()
    receitas = listar_receitas()

    if form.validate_on_submit():
        dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
        refeicoes = ["pequeno_almoço", "almoço", "jantar"]
        refeicoes_selecionadas = {}

        for dia in dias:
            for refeicao in refeicoes:
                chave = f"{dia}_{refeicao}"
                receita_id = request.form.get(chave)
                if receita_id:
                    index = dias.index(dia)
                    data_refeicao = form.data_inicio.data + timedelta(days=index)
                    refeicoes_selecionadas[(data_refeicao, refeicao)] = int(receita_id)

        plano = criar_plano_semanal(
            utilizador_id=session["user_id"],
            data_inicio=form.data_inicio.data,
            refeicoes_selecionadas=refeicoes_selecionadas,
        )

        flash("Plano criado com sucesso!", "success")
        return redirect(url_for("main.home"))

    return render_template("meal_plans/criar.html", form=form, receitas=receitas)


@meal_plans_bp.route("/meus", endpoint="meus_planos")
def meus_planos():
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para ver os seus planos.", "warning")
        return redirect(url_for("auth.login"))

    planos = obter_planos_do_utilizador(session["user_id"])
    return render_template(
        "meal_plans/meus.html", planos=planos, form_apagar=FormApagarPlano()
    )


@meal_plans_bp.route("/ver/<int:plano_id>")
def ver(plano_id):
    plano = obter_plano_completo(plano_id)
    if not plano or plano.utilizador_id != session["user_id"]:
        flash("Plano não encontrado.", "danger")
        return redirect(url_for("meal_plans.meus_planos"))

    return render_template(
        "meal_plans/ver.html", plano=plano, form_apagar=FormApagarPlano()
    )


@meal_plans_bp.route("/apagar/<int:plano_id>", methods=["POST"])
def apagar_plano(plano_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    form = FormApagarPlano()
    if not form.validate_on_submit():
        flash("Pedido inválido.", "danger")
        return redirect(url_for("meal_plans.meus_planos"))
    plano = obter_plano_completo(plano_id)
    if not plano or plano.utilizador_id != session["user_id"]:
        flash("Plano não encontrado ou acesso negado.", "danger")
        return redirect(url_for("meal_plans.meus_planos"))
    if eliminar_plano(plano_id):
        flash("Plano eliminado com sucesso.", "success")
    else:
        flash("Erro ao apagar plano.", "danger")
    return redirect(url_for("meal_plans.meus_planos"))


@meal_plans_bp.route("/editar/<int:plano_id>", methods=["GET", "POST"])
def editar_plano(plano_id):
    plano = obter_plano_completo(plano_id)
    if not plano or plano.utilizador_id != session["user_id"]:
        flash("Plano não encontrado ou acesso negado.", "danger")
        return redirect(url_for("meal_plans.meus_planos"))

    form = MealPlanForm(obj=plano)
    receitas = listar_receitas()

    dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    refeicoes = ["pequeno_almoço", "almoço", "jantar"]
    data_inicio = plano.data_inicio

    def get_id(plano, dia_data, refeicao):
        for entry in plano.refeicoes:
            if entry.data_refeicao == dia_data and entry.refeicao_tipo == refeicao:
                return entry.receita_id
        return ""

    grelha_editar = []
    for idx, dia_nome in enumerate(dias_semana):
        dia_data = data_inicio + timedelta(days=idx)
        linha = {"nome": dia_nome.capitalize(), "data": dia_data, "refeicoes": {}}
        for refeicao in refeicoes:
            linha["refeicoes"][refeicao] = get_id(plano, dia_data, refeicao)
        grelha_editar.append(linha)

    if request.method == "POST" and form.validate():
        print("==== request.form ====")
        print(request.form)

        refeicoes_selecionadas = {}
        for chave, receita_id in request.form.items():
            print(f"Processando campo: {chave} = {receita_id}")
            if chave in ["csrf_token", "data_inicio"] or receita_id == "":
                continue
            if "-" not in chave:
                print(f"Campo ignorado (sem hífen): {chave}")
                continue
            try:
                data_str, refeicao = chave.rsplit("-", 1)  # <-- USAR rsplit!
                print(f"data_str: {data_str} | refeicao: {refeicao}")
                data_refeicao = datetime.strptime(data_str, "%Y-%m-%d").date()
                print(f"data_refeicao convertido: {data_refeicao}")

                refeicoes_selecionadas[(data_refeicao, refeicao)] = int(receita_id)
                print(f"Guardado: ({data_refeicao}, {refeicao}): {receita_id}")
            except Exception as e:
                print(f"Erro ao processar campo {chave}: {e}")
                continue

        print("==== refeicoes_selecionadas ====")
        print(refeicoes_selecionadas)

        atualizar_plano_semanal(plano, form.data_inicio.data, refeicoes_selecionadas)
        flash("Plano atualizado com sucesso.", "success")
        return redirect(url_for("meal_plans.ver", plano_id=plano_id))

    return render_template(
        "meal_plans/editar.html",
        form=form,
        receitas=receitas,
        plano=plano,
        grelha_editar=grelha_editar,
        timedelta=timedelta,
        datetime=datetime,
    )


@meal_plans_bp.route("/exportar_pdf/<int:plano_id>", endpoint="exportar_pdf")
def exportar_pdf(plano_id):
    plano = obter_plano_completo(plano_id)
    if not plano or plano.utilizador_id != session["user_id"]:
        flash("Plano não encontrado ou acesso negado.", "danger")
        return redirect(url_for("meal_plans.meus_planos"))

    try:
        pdf_bytes = exportar_plano_para_pdf(plano)
    except OSError:
        flash(
            "Exportação para PDF ainda não está disponível nesta plataforma (Railway), devido a incompatibilidade técnica com a biblioteca PDFKit.",
            "warning",
        )
        return redirect(url_for("meal_plans.ver", plano_id=plano_id))
    except Exception as e:
        flash(
            f"Ocorreu um erro ao exportar o PDF: {str(e)}",
            "danger",
        )
        return redirect(url_for("meal_plans.ver", plano_id=plano_id))

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name="plano_semanal.pdf",
        mimetype="application/pdf",
    )
