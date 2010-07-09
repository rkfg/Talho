# -*- coding: utf-8 -*-
import random

def main(bot, text):
    if random.random() > 0.5:
        return

    if text.lower().startswith(u"а то") and len(text) < 6:
        return random.choice((u"лол, и правда ведь!", u"НЕ ТО!", u"I WANT TO A TO", u"you bet!"))

def info(bot):
    return('', 10, main)
