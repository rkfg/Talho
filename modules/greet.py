# -*- coding: utf-8 -*-
import random

def main(bot, text):

    greets = {
        u'суп': 'soup',
        u'супец': 'soup',
        u'супцы': 'soup',
        u'щи': 'soup',
        u'борщ': 'soup',
        u'здрасьте': 'hi',
        u'здрасте': 'hi',
        u'йоу': 'yo',
        u'йо': 'yo',
        u'ё': 'yo',
        u'ёу': 'yo',
        u'ку': 'q',
        u'куку': 'q',
        u'а': 'a',
        u'я': 'r',
        u'r': 'r',
        u'а то': 'ato',
        u'а то!': 'ato'
        }

    answers = {
        'soup': (u'борщ', u'щи', u'рассольник', u'уха'),
        'hi': (u'хуец покрасьте', u'пизду раскрасьте', u'namaste!'),
        'yo': (u'йоу, братан!', u'хуйоу'),
        'q': (u'ку-ку'),
        'a': (u'хуй на!',),
        'r': (u'головка от часов "Заря"', u'NO R', u'R!', u'дуло от ружья!', u'сосала у коня!', u'и три богатыря', u'якало несчастное.'),
        'ato': (u"лол, и правда ведь!", u"НЕ ТО!", u"I WANT TO A TO", u"you bet!")
        }

    text = text.lower()
    for greeting in greets:
        if text == greeting:
            if random.random() > 0.7:
                return

            return random.choice(answers[greets[greeting]])

def info(bot):
    return('', 10, main)
