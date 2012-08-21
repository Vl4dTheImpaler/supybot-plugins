###
# plugins/Pastebin.py by SpiderDave
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import os
import urllib, urllib2

def pastehtml(text):
    """<text>
    
    post <text> to pastehtml.
    """
    threaded=True
    api_url = 'http://pastehtml.com/upload/create?input_type=txt&result=address'
    #valid_paste_expire_dates = ('never', '10min', '1hour', '1day', '1month', '1year')
    
    values = {'txt' : text}

    data = urllib.urlencode(values)
    requ = urllib2.Request(api_url, data)
    response = urllib2.urlopen(requ)
    the_page = response.read()
    return the_page


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
