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