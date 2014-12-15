# -*- coding: utf8 -*-

"""
    The ``dbs`` module
    ===================

    Contain all functions to access to main site db or any sql-lite db, in a secure way
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


def create_session(engine_uri, echo=True):
    engine = sqlalchemy.create_engine(engine_uri, echo=echo)
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return session


def auto_map_orm(engine):
    base_class = automap_base()
    base_class.prepare(engine, reflect=True)
