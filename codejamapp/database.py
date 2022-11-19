import os
from flask import current_app, Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///" + os.path.join(current_app.config['DATABASE']))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initializes the database."""
    import codejamapp.models
    Base.metadata.create_all(bind=engine)

def close_db(e=None):
    db_session.remove()

def init_app(app: Flask):
    app.teardown_appcontext(close_db)