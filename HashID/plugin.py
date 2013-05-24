###
# Copyright (c) 2012, Vlad
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import supybot.ircmsgs as ircmsgs
import hashidentifier
import string, sys, time, urllib2, cookielib, re, random, threading, socket, os, subprocess

_ = PluginInternationalization('HashID')

@internationalizeDocstring
class HashID(callbacks.Plugin):
    """Add the help for "@plugin help HashID" here
    This should describe *how* to use this plugin."""
    threaded = True
    pass

    @internationalizeDocstring
    def hashid(self, irc, msg, args, text):
        reload(hashidentifier)
        nick = msg.nick
        network = irc.network
        channell = msg.args[0]
        if self.registryValue('channels', channell):
            unfinishedhash = text
        else: irc.error(nick + ", " + channell + " isn't registered in my config. Please contact my owner (Vlad) for more details", Raise=True)
        identifiedhash1, identifiedhash2 = hashidentifier.ident(unfinishedhash)
        if identifiedhash1 == "Not Found.":
            irc.error("I couldn't identify " + unfinishedhash)
        elif identifiedhash2 == "":
            irc.queueMsg(ircmsgs.privmsg(channell, "Possible Hashs for " + unfinishedhash + ":"))
            irc.queueMsg(ircmsgs.privmsg(channell, "[+] " + identifiedhash1))
        else: 
            irc.queueMsg(ircmsgs.privmsg(channell, "Possible Hashs for " + unfinishedhash + ":"))
            irc.queueMsg(ircmsgs.privmsg(channell, "[+] " + identifiedhash1))
            irc.queueMsg(ircmsgs.privmsg(channell, "[+] " + identifiedhash2))
    hashid = wrap(hashid, ['anything'])

Class = HashID


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
