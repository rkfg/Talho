# -*- coding: utf-8 -*-
import random

def main(bot, text):

    greets = {
        u'суп' : 'soup',
        u'супец' : 'soup',
        u'супцы' : 'soup',
        u'щи' : 'soup',
        u'борщ' : 'soup',
        u'здрасьте' : 'hi',
        u'здрасте' : 'hi',
        u'йоу' : 'yo',
        u'йо' : 'yo',
        u'ё' : 'yo',
        u'ёу' : 'yo',
        u'ку' : 'yo',
        u'куку' : 'yo',
        }

    answers = {
        'soup' : (u'борщ', u'щи', u'рассольник', u'уха'),
        'hi' : (u'хуец покрасьте', u'пизду раскрасьте', u'namaste!'),
        'yo' : (u'йоу, братан!', u'хуйоу', u'ку-ку'),
        }

    text = text.lower()
    for greeting in greets:
        if text == greeting:
            if random.random() > 0.7:
                return

            return random.choice(answers[greets[greeting]])

def info(bot):
    return('', 10, main)
