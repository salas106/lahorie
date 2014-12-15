# -*- coding: utf8 -*-

"""
    The ``test`` plugin
    ===================

    Test module from irc3.readthedocs.org.
    Intend to be modified for test version. So not versioned.
"""

__author__ = 'Salas'
__copyright__ = 'Copyright 2014 LTL'
__credits__ = ['Salas']
__license__ = 'MIT'
__version__ = '0.2.0'
__maintainer__ = 'Salas'
__email__ = 'Salas.106.212@gmail.com'
__status__ = 'Pre-Alpha'

import irc3
from irc3.plugins.command import command


@irc3.plugin
class MyPlugin:
    """A plugin is a class which take the irc-ltl-framework as argument
    """

    requires = [
        'irc3.plugins.core',
        'irc3.plugins.userlist',
        'irc3.plugins.command',
        'irc3.plugins.human'
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    def connection_made(self):
        """triggered when connection is up"""

    def server_ready(self):
        """triggered after the server sent the MOTD (require core plugin)"""

    def connection_lost(self):
        """triggered when connection is lost"""

    @irc3.event(irc3.rfc.JOIN)
    def welcome(self, mask, channel):
        """Welcome people who join a channel"""
        if mask.nick != self.bot.nick:
            self.bot.call_with_human_delay(
                self.bot.privmsg, channel, 'Welcome %s!' % mask.nick)
        else:
            self.bot.call_with_human_delay(
                self.bot.privmsg, channel, "Hi guys!")

    @command
    def echo(self, mask, target, args):
        """Echo command

            %%echo <words>...
        """
        self.bot.privmsg(mask.nick, ' '.join(args['<words>']) + ' ' + mask.nick + '!' + mask.host)

    @command
    def stats(self, mask, target, args):
        """Show stats of the channel using the userlist plugin

            %%stats [<channel>]
        """
        if args['<channel>']:
            channel = args['<channel>']
            target = mask.nick
        else:
            channel = target
        if channel in self.bot.channels:
            channel = self.bot.channels[channel]
            message = '{0} users'.format(len(channel))
            for mode, nicknames in sorted(channel.modes.items()):
                message += ' - {0}({1})'.format(mode, len(nicknames))
            self.bot.privmsg(target, message)

    @irc3.extend
    def my_usefull_method(self):
        """The extend decorator will allow you to call::

            bot.my_usefull_method()

        """
