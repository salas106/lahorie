# -*- coding: utf8 -*-

"""
    The ``common`` plugin
    =====================

    This plugin except to define the normal reactions on error.
"""

import irc3
import irc3.rfc


@irc3.plugin
class MyPlugin:
    """
        A plugin is a class which take the irc-ltl-framework as argument
    """

    requires = [
        'irc3.plugins.core'
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.ERR_NICKNAMEINUSE)
    def re_nick(self):
        pass