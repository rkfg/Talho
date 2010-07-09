# -*- coding: utf-8 -*-

import random

def main(bot, args):
	'''рассказать смешную историю про Кагами'''
	return bot.paste[random.randint(0, len(bot.paste) - 1)][:-1]
	
if __name__ == "__main__":
	print main(None, None)

def info(bot):
   fp = open("kagami.txt", "r")
   bot.paste = []
   for line in fp:
      bot.paste.append(line)
   fp.close()
   return ((u"kag", u"лфп", u"каг"), 10, main)
