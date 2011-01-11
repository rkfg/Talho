# -*- coding: utf-8 -*-

import urllib2
import socket
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from cgi import escape
from misc import _
import datetime

def main(bot, args):
	'''Ответить слушателю. Параметры: <user_id> <message>'''
	ans_file = "/home/eurekafag/data/www/radioanon.ru/answers.html"
	message_limit = 140
	if len(args) < 2:
		return
	if len(args[0]) != 10:
		return _("incorrect name entered, should be 10 symbols.")
        to = ">>" + args[0]
        message = " ".join(args[1:])
	if len(message) > message_limit:
		return _("too long answer, should be less than %d symbols, you entered %d symbols.") % (message_limit, len(message))
        soup = BeautifulSoup(open(ans_file, "r"))
	posts = soup.findAll('p')
	new_post = Tag(soup, 'p')
	user_id = Tag(soup, 'span', [('id', 'user_id')])
	user_id.insert(0, escape(to))
	new_post.insert(0, '[' + datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S") + ']')
	new_post.insert(1, user_id)
	new_post.insert(2, escape(message))
	posts[0].parent.insert(2, new_post)
	if len(posts) > 9:
		posts[len(posts) - 1].extract()

	f = open(ans_file, "w")
	f.write(soup.prettify())
	f.close()
        
        return _("sent.")

def info(bot):
    return (("a", u"ф"), 9, main)
