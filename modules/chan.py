# -*- coding: utf-8 -*-

import random, re

def main(bot, text):
    text = text.lower()
    if random.random() < 0.5 and re.search(ur'([^a-zа-я\-]|^)тян([^a-zа-я]|$)', text):
        return random.choice((u'тян? Крутой Петян!', u'тян? Смешной Галустян!', u'тян? Тигран Кеосаян!', u'тян? Говна ням-ням!', u'пошёл ты нахуй со своей тян!', u'тян? Хуян!', u'тян? Ну ты и Петросян.', u'тян? Ебись конём в пукан!', u'тян? Сосни хуйца, еблан.', u'тян? Да заебал уже, быдлан!', u'тян? Говна стакан!', u'тян? Нашествие инопланетян!', u'тян? Боян!', u'тян? http://www.komiinform.ru/services/persons/190/'))
    
def info(bot):
    return('', 10, main)
