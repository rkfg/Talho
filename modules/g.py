# -*- coding: utf-8 -*-

import urllib
import re
import misc
from misc import _
from simplejson import loads

def main(bot, args):
    '''g [site] <query>\nSearch on google.\nSite:
v - ru.wikipedia.org
w - en.wikipedia.org
lm - lurkmore
wa - world-art.ru
ad - anidb.info
ed - encyclopediadramatica
y - youtube.com'''

    if not args: return

    site = ''
    if args[0] == 'v':
        site = 'ru.wikipedia.org'
    elif args[0] == 'w':
        site = 'en.wikipedia.org'
    elif args[0] == 'lm':
        site = 'lurkmore.ru'
    elif args[0] == 'wa':
        site = 'world-art.ru'
    elif args[0] == 'ad':
        site = 'anidb.info'
    elif args[0] == 'ed':
        site = 'encyclopediadramatica.com'
    elif args[0] == 'y':
        site = 'youtube.com'

    if site:
        if len(args) == 1: return
        site = 'site:%s ' %site
        args = args[1:]

    return google(site + ' '.join(args), bot)

def google(query, bot):
    query = urllib.quote(query.encode('utf-8'))
    try:
        if "google_key" in bot.settings:
            google_key = "&key=" + bot.settings["google_key"]
        else:
            google_key = ""
        data = misc.readUrl('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&hl=ru%s' % (query, google_key), None, bot)
        if not data: return 'can\'t get data'
    except:
        return _("google is not available, sorry.")

    try:
    	convert = loads(data)
	results = convert['responseData']['results']
	if not results: return 'not found'

    	url = urllib.unquote(results[0]['url'])
    	title = results[0]['titleNoFormatting']
    	content = results[0]['content']
    	text = '%s\n%s\n%s' %(title, content, url)

    	text = re.sub('<b>|</b>', '', text)
    	text = re.sub('   ', '\n', text)
	text = text.replace(u'\ufeff', '')

    	return text
    except:
    	return 'error'

def info(bot):
    return ((u"g", u"г", u"п"), 10, main)
