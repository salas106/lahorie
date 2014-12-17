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
conf = utils.config.get_config(config_prefix='plugin_info')

# http://docs.sqlalchemy.org/en/latest/dialects/index.html
engine, session = sql.create_engine_session(conf['db'])
Base = sql.auto_map_orm(engine)

Users = Base.classes.users_main
Permissions = Base.classes.permissions


class ListUsernameByRank(set):
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

    @classmethod
    def get_by_rank_name(cls, rank_name, init_set=None):
        """
        Allow a name as admin rather than an class level
        """
        rank_names = conf['ranks']
        min_rank, max_rank = rank_names.get(rank_name, (0, 1))
        cls.__init__(min_rank, max_rank, init_set)


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


@irc3.plugin
class Info():
    requires = [
        'irc3.plugins.core',
        'plugins.info'
    ]

    @irc3.extend
    def get_user(self, username):
        return User(username)

    @irc3.extend
    def list_username_by_rank_name(self, rank_name):
        return ListUsernameByRank.get_by_rank_name(rank_name)
