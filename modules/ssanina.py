# -*- coding: utf-8 -*-

import random

def main(bot, text):
    ssanina = (u'ССАНNНА', u'ШТАНNНА', u'КОНNНА', u'ГОВНNНА', u'БЕЗНОГNМ')

    if random.random() < 0.0001:
        return u'\n' * 100 + random.choice(ssanina)

def info(bot):
    return('', 10, main)
