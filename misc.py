# -*- coding: utf-8 -*-

import urllib2
import re
from lxml import etree
import socket
import gettext
import chardet
import httplib

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB;'+\
                        'rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4'

def force_unicode(string, encoding='utf-8'): #{{{
    if type(string) is str:
        string = string.decode(encoding)
    if type(string) is not unicode:
        string = unicode(string)
    return string
#}}}

def readUrl(url, cookies=None, bot=None): #{{{
    parsedurl = re.search('http://([^/]+)/?(.*)', url)
    if parsedurl and len(parsedurl.groups()) > 0:
        c = httplib.HTTPConnection(parsedurl.group(1))
	c.request('HEAD', '/' + parsedurl.group(2))
	r = c.getresponse()
	if str(r.status)[0] != '2':
	    return None

	if not r.getheader('Content-type').startswith('text/'):
	    return None

    try:
        if url.startswith('http://vkontakte.ru') or url.startswith('http://www.vkontakte.ru'):
            if bot:
                headers['Cookie'] = bot.settings["vkontakte_cookies"]
        if cookies:
            headers['Cookie'] = cookies
        
        request = urllib2.Request(url.encode('utf-8'), None, headers)
        link = urllib2.urlopen(request, timeout = 5)
	data = link.read()
	return data
    except:
        return None
#}}}

def getImgXML(img_url, img_src): #{{{
    img_url = re.sub('"|\'|<|>', '', img_url)
    img_src = re.sub('"|\'|<|>', '', img_src)
    img_url = re.sub('&', '&amp;', img_url)
    img_src = re.sub('&', '&amp;', img_src)

    return '<html xmlns=\'http://jabber.org/protocol/xhtml-im\'>' +\
           '<body xml:lang=\'en-US\' xmlns=\'http://www.w3.org/1999/xhtml\'>' +\
           '<a href=\'%s\'><img alt=\'img\' src=\'%s\' /></a>' %(img_url, img_src) +\
           '</body>' +\
           '</html>'
#}}}

def getTitle(link, bot): #{{{
    if re.search('^http://danbooru\.donmai\.us', link) or re.search('^http://(www\.)?gelbooru\.com', link):
        return ''
    else:
        try:
            data = readUrl(link, None, bot)
	    if "opennet.ru" in link:
	        data_enc = data.decode('koi8-r')
            else:
                try:     data_enc = data.decode('utf-8')
                except:  data_enc = data.decode('cp1251')
            return etree.HTML(data_enc).find('*//title').text.strip().replace('\t', '').replace('\n', ' ')
        except:
            return ''
#}}}

def makeTiny(link, bot): #{{{
    url = 'http://tinyurl.com/api-create.php?url=%s' %link.encode('utf-8')
    try:
        return readUrl(url, None, bot)
    except:
        return ''
#}}}

def _(text):
    return gettext.gettext(text).decode('utf-8')

