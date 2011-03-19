# -*- coding: utf-8 -*-

import urllib2
import socket
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from cgi import escape
from misc import _
from hashlib import md5
import datetime

def main(bot, args):
	'''формат: rb <N> [M]
Удалить сообщение #N, либо с N по M.'''
	if len(args) < 1 or len(args) > 2:
		return
	try:
		rollback_to = int(args[0])
		if len(args) == 2:
			rollback_from = rollback_to
			rollback_to = int(args[1])
		else:
			rollback_from = rollback_to
	except:
		return

	if rollback_from < 1 or rollback_to > 9 or rollback_to < rollback_from:
		return
	
        soup = BeautifulSoup(open(bot.settings["ans_file"], "r"))
	posts = soup.findAll('p')
	if rollback_to > len(posts):
		return _("some of those posts don't exist.")
	for i in xrange(rollback_from - 1, rollback_to):
		posts[i].extract()

	f = open(ans_file, "w")
	f.write(soup.prettify())
	f.close()
        
        return _("done.")

def info(bot):
    return (("rb", u"ки"), 0, main)
