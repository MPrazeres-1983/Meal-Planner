from app.models.recipe import Recipe
from app.db import db
from app.models import BlockedRecipe
from sqlalchemy import or_, select
from flask import session
from app.models.meal_plan import MealEntry


def criar_receita(dados, utilizador_id, publica_quando_aprovada=False):
    titulo = dados.get("titulo", "").strip().title()
    descricao = dados.get("descricao", "").strip()
    ingredientes = dados.get("ingredientes", "").strip()
    instrucoes = dados.get("instrucoes", "").strip()
    tempo = dados.get("tempo_preparacao")
    dificuldade = dados.get("dificuldade")
    tags = dados.get("tags", "").strip()
    categoria_id = dados.get("categoria_id")

    if not (titulo and ingredientes and instrucoes and categoria_id):
        return None

    nova_receita = Recipe(
        titulo=titulo,
        descricao=descricao,
        ingredientes=ingredientes,
        instrucoes=instrucoes,
        tempo_preparacao=tempo,
        dificuldade=dificuldade,
        tags=tags,
        categoria_id=categoria_id,
        publicada=dados.get("publicada", False),
        aprovada=dados.get("aprovada", False),
        fonte=dados.get("fonte", "utilizador"),
        utilizador_id=utilizador_id,
        publica_quando_aprovada=publica_quando_aprovada,
    )
    db.session.add(nova_receita)
    db.session.commit()
    return nova_receita


def aprovar_receita(receita_id):
    receita = db.session.get(Recipe, receita_id)
    if receita:
        receita.publicada = receita.publica_quando_aprovada
        receita.aprovada = True
        db.session.commit()
    return receita


def eliminar_receita(receita_id):
    # Verifica se existe MealEntry associada à receita
    existe_referencia = MealEntry.query.filter_by(receita_id=receita_id).first()
    if existe_referencia:
        return (
            False,
            "Não é possível eliminar a receita porque está associada a um ou mais planos semanais.",
        )
    receita = db.session.get(Recipe, receita_id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
        return True, None
    return False, "Receita não encontrada."


def listar_receitas():
    user_id = session.get("user_id")
    nivel = session.get("user_nivel")

    query = Recipe.query

    if nivel == 3:
        # Admin vê todas
        return query.order_by(Recipe.data_submetida.desc()).all()

    if user_id:
        # Utilizador: públicas ou as suas próprias (mesmo privadas)
        query = query.filter(
            or_(Recipe.publicada == True, Recipe.utilizador_id == user_id)
        )

        # Bloqueadas: subquery de receitas bloqueadas
        subquery = select(BlockedRecipe.receita_id).where(
            BlockedRecipe.utilizador_id == user_id
        )

        query = query.filter(~Recipe.id.in_(subquery))

        return query.order_by(Recipe.data_submetida.desc()).all()
    else:
        # Visitante: só públicas
        query = query.filter_by(publicada=True)

    return query.order_by(Recipe.data_submetida.desc()).all()


def buscar_receitas(filtros):
    query = Recipe.query.filter_by(publicada=True)

    if "search" in filtros:
        termo = f"%{filtros['search']}%"
        query = query.filter(
            or_(Recipe.titulo.ilike(termo), Recipe.descricao.ilike(termo))
        )

    if "categoria" in filtros:
        query = query.filter(Recipe.categoria_id == filtros["categoria"])

    if "tags" in filtros:
        termo = f"%{filtros['tags']}%"
        query = query.filter(Recipe.tags.ilike(termo))

    if "tempo_maximo" in filtros:
        query = query.filter(Recipe.tempo_preparacao <= filtros["tempo_maximo"])

    return query.order_by(Recipe.data_submetida.desc()).all()


def obter_receita_por_id(receita_id):
    return Recipe.query.get(receita_id)


def listar_receitas_por_utilizador(utilizador_id):
    return (
        Recipe.query.filter_by(utilizador_id=utilizador_id)
        .order_by(Recipe.data_submetida.desc())
        .all()
    )


def listar_pendentes():
    return (
        Recipe.query.filter_by(aprovada=False)
        .order_by(Recipe.data_submetida.asc())
        .all()
    )
