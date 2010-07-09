# -*- coding: utf-8 -*-

def main(bot, args):
	'''добавить смешную историю про Кагами'''
	fp = open("kagami.txt", "a")
	phrase = " ".join(args)
	fp.write(phrase.encode("utf-8") + "\n")
	bot.paste.append(phrase + "\n")
	fp.close()
	return "фраза \"" + phrase.encode("utf-8") + "\" добавлена в лексикон. "

if __name__ == "__main__":
	print main(None, ("Когами", "с", "потрохами"))

def info(bot):
    return (("kagadd",), 1, main)
