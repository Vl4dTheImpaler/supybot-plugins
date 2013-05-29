import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import supybot.ircmsgs as ircmsgs
import os, pbj, signal

def scan(text):
#	if errno == "1":
#		irc.error("One Nmap scan is already running", Raise=True)
#	else:
#		errno = "1"
	print text
	processname = "/usr/local/bin/nmap -T4 -A -v -Pn"
	for line in os.popen("ps xa"):
		fields = line.split()
		pid = fields[0]
		process = fields[4]
	if process.find(processname) > 0:
		irc.error("Nmap is already running!", Raise=True)
	else:
		result = pbj.pastehtml(os.system("/usr/local/bin/nmap -T4 -A -v -Pn %s" % text))
		result = result.replace('/view/', '/raw/')
#		errno = "0"
	return result
