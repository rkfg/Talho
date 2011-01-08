# -*- coding: utf-8 -*-

import urllib
from HTMLParser import HTMLParser
import time
from htmlentitydefs import name2codepoint

S_NOTHING, S_QUOTE, S_HEADING, S_QUOTE_TEXT, S_COMPLETE = range(5)
timeout = 30

class borParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.state = S_NOTHING
		self.quote = ""
		self.lasttime = 0
	
	def handle_starttag(self, tag, attrs):
		if self.state == S_COMPLETE:
			return

		if self.state == S_QUOTE_TEXT and (tag == "br" or tag == "p"):
			self.quote += u"\n"

		if self.state == S_NOTHING and tag == "div" and ("class", "text") in attrs:
			self.state = S_QUOTE
			return

		if self.state == S_QUOTE and tag == "h3":
			self.state = S_HEADING
			return

		if self.state == S_QUOTE and tag == "p" and ("class", "text") in attrs:
			self.state = S_QUOTE_TEXT
			return
		
	def handle_endtag(self, tag):
		if self.state == S_QUOTE_TEXT and tag == "p":
			self.state = S_COMPLETE
			return

		if self.state == S_HEADING and tag == "h3":
			self.state = S_QUOTE
			return

	def handle_data(self, data):
		if self.state == S_HEADING:
			self.quote = u"*" + data.decode("cp1251") + u"*\n\n"
			return

		if self.state == S_QUOTE_TEXT:
			self.quote += data.decode("cp1251")
			return

	def handle_entityref(self, name):
		if self.state == S_QUOTE_TEXT:
			self.quote += unichr(name2codepoint[name])
	

def main(bot, args):
	'''Выдать случайную цитату с ithappens.ru'''
	timespent = time.time() - parser.lasttime
	if timespent < timeout:
		return "До следующей цитаты " + str(round(timeout - timespent, 2)) + " сек."
	try:
		link = urllib.urlopen("http://ithappens.ru/story/" + str(args[0]))
	except (ValueError, IndexError):
		link = urllib.urlopen("http://ithappens.ru/random/")
	itpage = link.read()
	parser.quote = ""
	parser.state = S_NOTHING
	parser.feed(itpage)
	parser.lasttime = time.time()
	if parser.quote == "":
		return "Ошибка получения цитаты."
	else:
		return parser.quote

parser = borParser()
if __name__ == "__main__":
	print main(None, None)

def info(bot):
    return (("it", u"ит"), 10, main)
