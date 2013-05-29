import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import supybot.ircmsgs as ircmsgs
import os, pbj, signal, urllib2

def scan(text):
    try:
        inst = subprocess.Popen(text, stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      stdin=file(os.devnull))
        except OSError, e:
            irc.error('It seems the requested command was '
                      'not available (%s).' % e, Raise=True)
        result = inst.communicate()
        if result[1]: # stderr
            irc.error(' '.join(result[1].split()))
        if result[0]: # stdout
            response = result[0].split("\n");
            response = [l for l in response if l]
        result = pbj.pastehtml(response).replace('/view', '/raw/') #result = result.replace('/view/', '/raw/')
        if not "Starting Nmap" in urllib2.urlopen(result):
            result = "Error, I returned %r instead of a true scan."
    return result
