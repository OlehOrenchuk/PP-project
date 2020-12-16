# we create an engine using the connection string. To create an engine we use SQA's create_engine
from datetime import datetime

from sqlalchemy import create_engine
# make a session
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base
#from contextlib import contextmanager

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()
"""
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
"""

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()

