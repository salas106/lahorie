# -*- coding: utf8 -*-

"""
    The ``dbs`` module
    ===================

    Contain all functions to access to main site db or any sql-lite db, in a secure way
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import join

def create_engine_session(engine_url, echo=True):
    """
    Create a sql session

    engine is the rfc1738 compliant url
    http://docs.sqlalchemy.org/en/latest/dialects/index.html
    :param engine_url:
    :param echo:
    :return:
    """
    engine = sqlalchemy.create_engine(engine_url, echo=echo)
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return engine, session


def auto_map_orm(engine):
    base_class = automap_base()
    base_class.prepare(engine, reflect=True)

