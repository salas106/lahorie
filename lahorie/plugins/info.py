# -*- coding: utf8 -*-

"""
    The ``info`` plugin
    ===================
    
    It aims to provide user info taking into account gazelle paranoia.
"""

import irc3
import irc3.rfc

from utils import sql

import utils.config
conf = utils.config.get_config(config_prefix='plugin_authentication')

# http://docs.sqlalchemy.org/en/latest/dialects/index.html
engine, session = sql.create_engine_session(conf['db'])
Base = sql.auto_map_orm(engine)

Users = Base.classes.users_main
Permissions = Base.classes.permissions


class UsersGreaterThan(set):
    def __init__(self, min_rank, max_rank=None, init_set=None):
        if max_rank is None:
            max_rank = min_rank + 1
        self.borne = (min_rank, max_rank)
        # Care for the mutable
        if init_set is None:
            super().__init__()
        else:
            super().__init__(init_set)

    def retrieve(self):
        min_rank, max_rank = self.borne
        username = session.query(Users.username).\
            select_from(sql.join(Users, Permissions)).\
            filter(Permissions.Level >= min_rank,
                   Permissions.Level < max_rank).\
            all()
        self.union(username)

high_staff_users = UsersGreaterThan(0)


class User:
    def __init__(self, username):
        user_query_result = session.query(Users).\
            filter(Users.username == username).\
            first()
        if user_query_result is not None:
            self.id = user_query_result.ID
            self.irc_key = user_query_result.IRCKey
            self.enabled = user_query_result.Enabled
            self.user_class = user_query_result.Class
            self.permission_id = user_query_result.PermissionID
        else:
            self.id = None
            self.irc_key = None
            self.enabled = None
            self.user_class = None
            self.permission_id = None

    def information(self):
        pass  # TODO

    def validate(self, irc_key):
        if self.id is None:
            return False, "User not found"
        elif self.enabled != 1:
            return False, "User disabled"
        elif self.irc_key == '':
            return False, "Irc key not initialized"
        elif self.irc_key != irc_key:
            return False, "Wrong key"
        else:
            return True, "Match"