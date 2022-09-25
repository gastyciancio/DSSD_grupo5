import pymysql
from flask_sqlalchemy import SQLAlchemy

from flask import current_app
from flask import g
from flask import cli

db=SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)

def config_db(app):
    
    @app.before_first_request
    def init_database():
        db.create_all()
 
    @app.teardown_request
    def close_session(exception=None):
        db.session.remove()

def connection():
    if "db_conn" not in g:
        conf = current_app.config
        g.db_conn = pymysql.connect(
            host=conf["DB_HOST"],
            user=conf["DB_USER"],
            password=conf["DB_PASS"],
            db=conf["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,
        )
    return g.db_conn