# -*- coding: utf-8 -*-

import urllib
from HTMLParser import HTMLParser
import time
import random
from htmlentitydefs import name2codepoint

S_NOTHING, S_QUOTE, S_QUOTE_TEXT, S_COMPLETE = range(4)
timeout = 30

class borParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.state = S_NOTHING
		self.quote = u"\n"
		self.lasttime = 0
	
	def handle_starttag(self, tag, attrs):
		if self.state == S_COMPLETE:
			return

		if self.state == S_QUOTE_TEXT and (tag == "br" or tag == "p"):
			self.quote += u"\n"

		if tag == "div":
			if ("class", "q") in attrs:
				self.state = S_QUOTE
			else:
				if self.state == S_QUOTE and attrs == []:
					if parser.quotenum == 0:
						self.state = S_QUOTE_TEXT
					else:
						parser.quotenum -= 1
						self.state = S_NOTHING

	def handle_endtag(self, tag):
		if self.state == S_QUOTE_TEXT and tag == "div":
			self.state = S_COMPLETE

	def handle_data(self, data):
		if self.state == S_QUOTE_TEXT:
			if "document.phpAds_used" in data:
				self.state == S_NOTHING
				self.quotenum == 1
			else:
				self.quote += data.decode("cp1251")

	def handle_entityref(self, name):
		if self.state == S_QUOTE_TEXT:
			self.quote += unichr(name2codepoint[name])
	
def main(bot, args):
	'''Выдать случайную цитату с bash.org.ru'''
	borpage = ""
	timespent = time.time() - parser.lasttime
	if timespent < timeout:
		return "До следующей цитаты " + str(round(timeout - timespent, 2)) + " сек."
	try:
		link = urllib.urlopen("http://bash.org.ru/quote/" + str(args[0]))
		parser.quotenum = 0
	except (ValueError, IndexError):
		link = urllib.urlopen("http://bash.org.ru/random")
		parser.quotenum = random.randint(0, 30)
	borpage = link.read()
	parser.quote = u"\n"
	parser.state = S_NOTHING
	parser.feed(borpage.replace("</sc'+'ript>'", ""))
	if parser.quote == u"\n":
		return "Ошибка получения цитаты."
	else:
		parser.lasttime = time.time()
		return parser.quote

parser = borParser()
if __name__ == "__main__":
	print main(None, None)

def info(bot):
    return (("bor", u"бор"), 10, main)
