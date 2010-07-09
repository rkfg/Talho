# -*- coding: utf-8 -*-

import urllib2
import socket

def main(bot, args):
	'''Проверить, лежит ли сайт'''
	if not args:
		return
	try:
            link = urllib2.urlopen(urllib2.Request("http://downforeveryoneorjustme.com/" + args[0].encode("utf-8")), timeout = 20)
	    downfor = link.read()
	    return u"сайт " + args[0] + (u" в дауне" if "It's not just you!" in downfor else u" работает" if "It's just you" in downfor else u" не сайт вообще")
	except urllib2.URLError:
	    return u"ошибка запроса."

if __name__ == "__main__":
	print main(None, "adfsdf.com")

def info(bot):
    return (("d", u"д"), 10, main)
