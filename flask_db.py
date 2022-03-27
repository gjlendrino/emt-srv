from flask import g
from data_base_emt import DataBaseEMT


def get_db():
    if 'db' not in g:
        g.db = DataBaseEMT()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close_connection()


def init_app(app):
    app.teardown_appcontext(close_db)
