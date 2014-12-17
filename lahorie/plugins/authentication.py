# -*- coding: utf8 -*-

"""
    The ``authentication`` plugin
    =============================

    It aims to provide a secure and resilient way to auth user and invite them into invite only channels.
    It aims to save all the channels where the user want (and can) to be invited.
    It also aims to check if the user is ban or warned or chat limited.
"""
import re

import irc3
import irc3.rfc

import utils.config

conf = utils.config.get_config(config_prefix='plugin_authentication')


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


@irc3.plugin
class Authentication:
    """
        A plugin is a class which take the irc-ltl-framework as argument
    """

    requires = [
        'irc3.plugins.core',
        'plugins.info'
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.PRIVMSG)
    def on_msg(self, text, mask=None, target=None, client=None, **kw):
        if not target.is_channel:
            parse_regex = re.compile(r"^(enter)\s*"
                                     r"(?P<chans>(#\w+),\s?)*(#\w+)\s*"
                                     r"(?P<username>[a-zA-Z0-9]+)\s*"
                                     r"(?P<irc_key>[a-z0-9]{32})$",
                                     re.IGNORECASE)
            username = parse_regex.search(text).group('username')
            irc_key = parse_regex.search(text).group('irc_key')
            channels = parse_regex.search(text).group('chans')
            valid, new_ident, new_host, reason = self.validate(username, irc_key)
            if valid:
                self.bot.send('CHGDENT {0} {1}'.format(username, new_ident))
                self.bot.send('CHGHOST {0} {1}'.format(username, new_host))
                for chan in channels.sentence.replace(' ', '').split(','):
                    self.bot.send('SAJOIN {0} {1}'.format(username, chan))

    def validate(self, username, irc_key):
        user = self.get_user(username)
        valid = False
        new_ident = None
        new_host = None
        if user.id is None:
            reason = "User not found"
        elif user.enabled != 1:
            reason = "User disabled"
        elif user.irc_key == '':
            reason = "Irc key not initialized"
        elif user.irc_key != irc_key:
            reason = "Wrong key"
        else:
            valid = True
            rank = 'staff' if username in self.list_username_by_rank_name('staff') else 'user'
            new_ident = username
            new_host = "{1}.{3}".format(rank, conf['host'])
            reason = "Match"
        return valid, new_ident, new_host, reason