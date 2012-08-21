##
# Copyright (c) 2012, Dinosaur
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.ircdb as ircdb
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import urllib
import httplib
import linecache
import re

#targett="There is no current target"
#boosterr="There is no current booster"
#channell = msg.args[0]
#target_line = linecache.getline(channell, 1)
#booster_line = linecache.getline(channell, 2)
reasonn="No Reason"
capabilityneeded='op'

codes={"100":"Continue", "101":"Switching Protocols", "200":"Successful", "201":"Created", "202":"Accepted", "203":"Non-authoritative Information", "204":"No Content", "205":"Reset Content", "206":"Partial Content", "300":"Multiple Choices", "301":"Moved Permanently", "302":"Moved Temporarily", "303":"See Other Location", "304":"Not Modified", "305":"Use Proxy", "307":"Temporary Redirect", "400":"Bad Request", "401":"Not Authorized", "403":"Forbidden", "404":"Not Found", "405":"Method Not Allowed", "406":"Not Acceptable", "407":"Proxy Authentication Required", "408":"Request Timeout", "409":"Conflict", "410":"Gone", "411":"Length Required", "412":"Precondition Failed", "413":"Request Entity Too Large", "414":"Requests URI Is Too Long", "415":"Unsupported Media Type", "416":"Requested Range Not Satisfiable", "417":"Expectation Failed", "500":"Internal Server Error", "501":"Not Implemented", "502":"Bad Gateway", "503":"Service Unavailable", "504":"Gateway Timeout", "505":"HTTP Version Not Supported"}

class SiteCheck(callbacks.Plugin):
    """Checks a site's availability and returns relevant HTTP status code"""
    threaded = True
    pass

    def reasonset(self, irc, msg, args, text):
        """<reason>

        Sets a new reason"""
        network = irc.network
        channell = msg.args[0]
        nick = msg.nick
        global targett
        global boosterr
        global reasonn
        
        if channell in self.registryValue('channels').split(' '):
            global targett
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if nick in irc.state.channels[channell].ops:
            capability='ops'
            if not ircdb.checkCapability(msg.prefix, capability):
                irc.errorNoCapability(capability, Raise=True)
            target_line = linecache.getline(channell+network, 1).rstrip("\n")
            booster_line = linecache.getline(channell+network, 2).rstrip("\n")
            reason_line = linecache.getline(channell+network, 3).rstrip("\n")
            reasonn = text
            oldfile = open(channell+network, 'w')
            oldfile.write(target_line+"\n")
            oldfile.write(booster_line+"\n")
            oldfile.write(reasonn)
            oldfile.flush()
            linecache.clearcache()
            irc.reply('Done.')
    reasonset = wrap(reasonset, ['text'])

    def targetset(self, irc, msg, args, text):
        """<target>

        Sets a new target"""
        channell = msg.args[0]
        network = irc.network
        nick = msg.nick
        global targett
        global boosterr
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if channell in self.registryValue('channels').split(' '):
            global targett
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
        if nick in irc.state.channels[channell].ops:
            capability='ops'
            if not ircdb.checkCapability(msg.prefix, capability):
                irc.errorNoCapability(capability, Raise=True)
            
            target_line = linecache.getline(channell+network, 1).rstrip("\n")
            booster_line = linecache.getline(channell+network, 2).rstrip("\n")
            reason_line = linecache.getline(channell+network, 3).rstrip("\n")
            targett = text
            oldfile = open(channell+network, 'w')
            oldfile.write(targett+"\n")
            oldfile.write(booster_line+"\n")
            oldfile.flush()
            linecache.clearcache()
            irc.reply('Done.')        
    targetset = wrap(targetset, ['anything'])

    def boosterset(self, irc, msg, args, text):
        """<booster>

        Sets a new booster"""
        channell = msg.args[0]
        network = irc.network
        nick = msg.nick
        global targett
        global boosterr
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if msg.args[0] in self.registryValue('channels').split(' '):
            global targett
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
        if nick in irc.state.channels[channell].ops:
            capability='ops'
            if not ircdb.checkCapability(msg.prefix, capability):
                irc.errorNoCapability(capability, Raise=True)
            
            target_line = linecache.getline(channell+network, 1).rstrip("\n")
            booster_line = linecache.getline(channell+network, 2).rstrip("\n")
            reason_line = linecache.getline(channell+network, 3).rstrip("\n")
            boosterrx = text
            oldfile = open(channell+network, 'w')
            oldfile.write(target_line+"\n")
            oldfile.write(boosterrx+"\n")
            oldfile.flush()
            linecache.clearcache()
            irc.reply('Done.')
    boosterset = wrap(boosterset, ['anything'])

    def target(self, irc, msg, args):
        """Takes no arguments

        Returns target & booster (if applicable)"""
        network = irc.network
        channell = msg.args[0]
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if msg.args[0] in self.registryValue('channels').split(' '):
            target_line = linecache.getline(channell+network, 1).rstrip('\n')
            booster_line = linecache.getline(channell+network, 2).rstrip('\n')
            irc.reply('\002\0034TARGET: \002\0031%s | \002\0034BOOSTER: \002\0031%s' % (target_line, booster_line))
            linecache.clearcache()
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
    target = wrap(target)

    def reason(self, irc, msg, args):
        """Takes no arguments

        Returns reason for attack"""
        channell = msg.args[0]
        network = irc.network
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if msg.args[0] in self.registryValue('channels').split(' '):
            reason_line = linecache.getline(channell+network, 3).rstrip('\n')
            if reason_line == '':
                irc.error('No reason set! Please let an Op know about this error.', Raise=True)
            irc.reply('%s' % reason_line)
            linecache.clearcache()
        else: irc.error('Not a valid channel!', Raise=True)
    reason = wrap(reason)

    def check(self, irc, msg, args):
        """Takes no arguments

        Checks target's availability, and returns HTTP code, if you are op, use checksite for another site"""
        irc.reply('Plz wait a few seconds, the scan has commenced')
        network = irc.network
        channell = msg.args[0]
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if msg.args[0] in self.registryValue('channels').split(' '):
            global targett
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
        target_line = linecache.getline(channell+network, 1).rstrip('\n')
        taxxy = target_line
        if target_line == "There is no current target":
		    irc.error('No target set', Raise=True)
        count = taxxy.count('http://')
        if count == 0:
            taxxy = 'http://%s' % taxxy
        tax = taxxy[4]
        if tax != ":":
            taxxy = taxxy.replace ( 'http://', '')
            taxxy = 'http://%s' % taxxy
        try:
            status = (urllib.urlopen("%s" % taxxy).getcode())
        except StandardError:
            status = "Nothing"
        if status != "Nothing":
            message = (codes["%s" % status])
        else:
            message = "Site does not exist, or did not respond"
        import urllib2
        req = urllib2.Request("http://www.isup.me/%s" % taxxy)
        responselol = urllib2.urlopen(req)
        contentsz = responselol.read()
     	if "looks down" in contentsz:
            statuss = "\0031isup.me returns that \002%s \002is \002\0034DOWN " % taxxy
        else:
            statuss = "\0031isup.me returns that \002%s \002is \002\0033UP " % taxxy
        if status == 200:
            irc.reply("\0031\002%s \002looks \002\0033UP \002\0031from here, %s" % (taxxy, statuss))
        else:
            irc.reply("\0031\002%s \002may be \002\0034DOWN \002\0031 -----> Returned code \002%s: '%s'\002, %s" % (taxxy, status, message, statuss))
        linecache.clearcache()
    check = thread(wrap(check))

    def checksite(self, irc, msg, args, text):
        """<site>

        Checks a site's availability, and returns HTTP code"""

        nick = msg.nick
        network = irc.network
        channell = msg.args[0]
        if irc.network == "UniBG":
            return
        #if nick in self.registryValue('blacklist').split(' '):
             #irc.error("You've been blacklisted!", Raise=True
        if msg.args[0] in self.registryValue('channels').split(' '):
            global targett
        else: irc.error('Not a valid channel! Please contact Vlad', Raise=True)
        if nick in irc.state.channels[channell].ops:
            capability='ops'
        else: irc.error(nick + " you aren't op'd!", Raise=True)
        irc.reply('Plz wait a few seconds, the scan has commenced')
        taxxy = text
        count = text.count('http://')
        if count == 0:
            taxxy = 'http://%s' % taxxy
        tax = taxxy[4]
        if tax != ":":
            taxxy = taxxy.replace ( 'http://', '')
            taxxy = 'http://%s' % taxxy
        try:
            status = (urllib.urlopen("%s" % taxxy).getcode())
        except StandardError:
            status = "Nothing"
        if status != "Nothing":
            message = (codes["%s" % status])
        else:
            message = "Site does not exist, or did not respond"
        import urllib2
        req = urllib2.Request("http://www.isup.me/%s" % taxxy)
        responselol = urllib2.urlopen(req)
        contentsz = responselol.read()
     	if "looks down" in contentsz:
            statuss = "\0031isup.me returns that \002%s \002is \002\0034DOWN " % taxxy
        else:
            statuss = "\0031isup.me returns that \002%s \002is \002\0033UP " % taxxy
        if status == 200:
            irc.reply("\0031\002%s \002looks \002\0033UP \002\0031from here, %s" % (taxxy, statuss))
        else:
            irc.reply("\0031\002%s \002may be \002\0034DOWN \002\0031 -----> Returned code \002%s : '%s'\002, %s" % (taxxy, status, message, statuss))
    checksite = wrap(checksite, ['anything'])
	

Class = SiteCheck

