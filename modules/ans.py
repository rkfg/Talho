# -*- coding: utf-8 -*-

import urllib2
import socket
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from cgi import escape
from misc import _
from hashlib import md5
import datetime

def main(bot, args):
	'''Ответить слушателю. Параметры: <user_id> <message>
Если в качестве user_id указать восклицательный знак, сообщение будет выглядеть как объявление.'''
	ans_file = "/srv/radioanon.ru/htdocs/answers.html"
	syl = { '0' : 'be', '1' : 'sa', '2' : 'ko', '3' : 'pa', '4' : 're', '5' : 'du', '6' : 'ma', '7' : 'ne', '8' : 'wa', '9' : 'si', 'a' : 'to', 'b' : 'za', 'c' : 'mi', 'd' : 'ka', 'e' : 'ga', 'f' : 'no' }
	salt = "blablabla_enter_random_symbols_here"
	message_limit = 250
	userpost = ""
	if len(args) < 2:
		return
	if args[0] != "!":
		if len(args[0]) != 12:
			return _("incorrect name entered, should be 12 symbols.")
		check = md5()
		check.update(args[0][:8].encode('utf-8') + salt)
		if check.hexdigest()[:4] != args[0][8:12]:
			return _("incorrect name entered (checksum invalid).")
	
		to = ">>" + args[0]
		if args[0] in bot.usersposts:
			userpost = "<span class=\"userpost\">&gt; " + escape(bot.usersposts[args[0]]) + "</span><br/>"
	else:
		to = "!"
        message = " ".join(args[1:])
	if len(message) > message_limit:
		return _("too long answer, should be less than %d symbols, you entered %d symbols.") % (message_limit, len(message))
        soup = BeautifulSoup(open(ans_file, "r"))
	posts = soup.findAll('p')
	new_post = Tag(soup, 'p')
	user_id = Tag(soup, 'span', [('id', 'user_id')])
	if to != "!":
		user_id.insert(0, escape(to))
	else:
		user_id.insert(0, "<b>&gt;&gt;ОБЪЯВЛЕНИЕ&lt;&lt;</b>")
	new_post.insert(0, '[' + datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S") + ']')
	new_post.insert(1, user_id)
	new_post.insert(2, userpost + escape(message))
	if len(posts) > 0:
		posts[0].parent.insert(2, new_post)
	else:
		soup.find('h1').parent.insert(1, new_post)
	if len(posts) > 9:
		posts[len(posts) - 1].extract()

	f = open(ans_file, "w")
	f.write(soup.prettify())
	f.close()
        
        return _("sent.")

def info(bot):
    return (("a", u"ф"), 9, main)
