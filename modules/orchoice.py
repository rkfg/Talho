# -*- coding: utf-8 -*-

import random, re
import logging
from pymorphy import get_morph

morph = get_morph('dict')

def rev(x):
    revmap = { u"Я" : u"ТЫ", u"МЕНЯ" : u"ТЕБЯ", u"МНЕ" : u"ТЕБЕ", u"МНОЙ" : u"ТОБОЙ", u"МЫ": u"ВЫ", u"НАС": u"ВАС", u"НАМ": u"ВАМ", u"НАС": u"ВАС", u"НАМИ": u"ВАМИ" }
    for k, v in revmap.items():
        revmap[v] = k

    xstr = x.replace(',', '').replace('.', '')
    if xstr in revmap:
        return x.replace(xstr, revmap[xstr]).lower()

    global morph
    info = morph.get_graminfo(x)
    if len(info):
        cls = info[0]['class']
        if cls == u'Г':
            if u'1л' in info[0]['info']:
                x = morph.inflect_ru(x, u'2л')
            if u'2л' in info[0]['info']:
                x = morph.inflect_ru(x, u'1л')

    return x.lower()

def main(bot, text):
    if len(text) > 200:
        return
    answers = [u"думаю, что %s", u"есть мнение, и не только моё, что %s", u"по-моему, %s", u"мне кажется, %s", u"боженька говорит, %s", u"пацаны говорят, что %s", u"не исключено, что %s"]
    text = text.upper()
    choices = text.split(u" ИЛИ ")
    choices = [ c.strip().replace("?", "").replace("!", "").replace(u"Ё", u"Е") for c in choices ]
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
