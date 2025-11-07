from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Connect Flask with the database.
    Create tables in the database if they don't exist yet.
    """
    db.init_app(app)       # link this db object with Flask app
    with app.app_context():  # gives permission to access Flask resources
        db.create_all()    # create tables (like Account) in the database

def get_db_session():
    return db.session