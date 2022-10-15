from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Inicializacion de la base de datos"""

    db.init_app(app)
    config_db(app)


def config_db(app):
    """Configuracion de la base de datos"""

    @app.before_first_request
    def init_database():
        
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()