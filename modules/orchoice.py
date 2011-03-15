# -*- coding: utf-8 -*-

import random, re
import logging

def rev(x):
    revmap = { u"я" : u"ты", u"меня" : u"тебя", u"мне" : u"тебе", u"мной" : u"тобой", u"ты" : u"я", u"тебя" : u"меня", u"тебе" : u"мне", u"тобой" : u"мной" }
    xstr = x.replace(',', '').replace('.', '')
    if xstr in revmap:
        return x.replace(xstr, revmap[xstr])
    else:
        return x

def main(bot, text):
    if len(text) > 200:
        return
    answers = [u"думаю, что %s", u"есть мнение, и не только моё, что %s", u"по-моему, %s", u"мне кажется, %s", u"боженька говорит, %s", u"пацаны говорят, что %s", u"не исключено, что %s"]
    text = text.lower()
    choices = text.split(u" или ")
    choices = [ c.strip().replace("?", "").replace("!", "") for c in choices ]
    choices = filter(lambda x: x != "", choices)
    if len(choices) < 2:
        return None

    last = None
    moodaque = True
    for a in choices:
        if not last:
	    last = a
	else:
	    if last != a:
	        moodaque = False
	        break

    if moodaque:
        answer = u"ты мудак :cf:"
    else:
        answer = random.choice(choices)
        answer = ' '.join(map(rev, answer.split()))

    if answer.endswith(','):
        answer = answer[:-1]

    if not answer.endswith('.'):
        answer += '.'

    return random.choice(answers) % answer
    
def info(bot):
    return('', 10, main)

if __name__ == "__main__":
    print main(None, u"Хуй, говно и муравей или пизда залупа сыр   или очко рваное?")
    print main(None, u"Хуй или хуй")
    print main(None, u" или или ")
    print main(None, u"  ")
