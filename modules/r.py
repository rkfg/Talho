# -*- coding: utf-8 -*-
import random

def main(bot, args):
    if args:
        return
    return random.choice(("R", u"Я", "NO R", "NO U", "RRR", u"ЯЯЯ", "LOL R", ".\_/."))

def info(bot):
    return ((u"r", u"R", u"Я", u"я"), 10, main)
