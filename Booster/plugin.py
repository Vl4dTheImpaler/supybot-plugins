

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import string, sys, time, urllib2, cookielib, re, random, threading, socket, os, subprocess
import pbj

url = "put booster url here"

class Booster(callbacks.Plugin):
    """Add the help for "@plugin help Booster" here
    This should describe *how* to use this plugin."""
    threaded = True

    def makebooster(self, irc, msg, args, text):
        reload(pbj)
        nick = msg.nick
        channell = msg.args[0]
        if nick in irc.state.channels[channell].halfops:
            capability='halfops'
            if not ircdb.checkCapability(msg.prefix, capability):
                irc.errorNoCapability(capability, Raise=True)
        irc.reply('Booster is on its way!')      
        req = urllib2.Request(url % text)
        responselol = urllib2.urlopen(req)
        contentsz = responselol.read()
        rawr = pbj.pastehtml(contentsz)
        rawr = rawr.replace('/view/', '/raw/')
        irc.reply(rawr)
    makebooster = wrap(makebooster, ['anything'])

Class = Booster


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
