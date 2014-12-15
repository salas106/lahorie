# -*- coding: utf8 -*-

"""
    The ``embed`` plugin
    ===================

    Look main chan public message and post some metadata about the contents using embedly service api.
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
import re
import embedly

import utils.config

# https://gist.github.com/dperini/729294
url_re = re.compile(r".*(?P<url>(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)"
                    r"(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
                    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|"
                    r"1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
                    r"{2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1"
                    r"-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-"
                    r"\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-"
                    r"\uffff]{2,})))(?::\d{2,5})?(?:/\S*)).*", re.IGNORECASE | re.UNICODE)

conf = utils.config.get_config(config_prefix='plugin_embed')


@irc3.plugin
class MyPlugin:
    """A plugin is a class which take the irc-ltl-framework as argument
    """

    requires = [
        'irc3.plugins.core'
    ]

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log
        self.embed_client = embedly.Embedly(conf['api']['key'])

    @irc3.event((r':(?P<mask>\S+) PRIVMSG (?P<target>\S+) '
                 r':(?P<text>.+)'))
    def url_pasted(self, text, mask=None, target=None, client=None, **kw):
        if target.is_channel:
            if url_re.match(text):
                url = url_re.search(text).group('url')
                self.do_embed(url, target)

    def do_embed(self, url, channel):
        embed_object = self.embed_client.oembed(url)
        self.bot.privmsg(channel, "\u0002\u000304[{0}]\u0002\u0003 {1}"
                                  " ".format(embed_object['type'],
                                             ' - '.join(['\u000309{}\u0003'.format(embed_object.get('author_name', '')),
                                                         '\u001d{}\u001d'.format(embed_object.get('title', ''))])))