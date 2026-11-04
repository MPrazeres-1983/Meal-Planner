from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.db import db
from datetime import datetime, timedelta, timezone

# Importar os blueprints
from app.routes.auth import auth_bp
from app.routes.recipes import recipes_bp
from app.routes.meal_plans import meal_plans_bp
from app.routes.admin import admin_bp
from app.routes.main import main_bp
from app.routes.categories import categories_bp
from app.routes.favorites import favorites_bp
from app.routes.blocked import blocked_bp


# Instância de proteção CSRF
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    from config import Config
    Config.init_app(app)

    csrf.init_app(app)
    db.init_app(app)

    @app.before_request
    def check_current_account():
        """Reject invalidated sessions and refresh permissions from the DB."""
        from flask import session, request, redirect, url_for
        from app.models.user import User

        user_id = session.get("user_id")
        if user_id is None:
            return None
        user = db.session.get(User, user_id)
        if user is None or not user.ativo:
            session.clear()
            # Logging in or viewing public pages must remain possible.
            if request.endpoint and (
                request.endpoint.startswith("auth.")
                or request.endpoint == "static"
            ):
                return None
            return redirect(url_for("auth.login"))

        # The role cached in the signed cookie is not an authority.
        session["user_nivel"] = user.nivel
        session["user_nome"] = user.nome
        return None

    # Registo dos blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(meal_plans_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(blocked_bp)

    # Adicionar filtros personalizados para templates

    @app.template_filter("dias_desde")
    def dias_desde(data):
        """Calcula o número de dias desde uma data até hoje."""
        if data:
            # Se não tiver timezone, assume UTC (evita erro do naive vs aware)
            if data.tzinfo is None:
                data = data.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - data).days
        return 0

    # Adicionar funções globais para templates
    @app.template_global()
    def now():
        """Retorna a data e hora atual."""
        return datetime.now()

    # Adicionar timedelta como global para cálculos de data nos templates
    app.jinja_env.globals["timedelta"] = timedelta

    return app
