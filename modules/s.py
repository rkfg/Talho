# -*- coding: utf-8 -*-

import radio

def main(bot, args):
    if args: return

    info, list = radio.getRadioState()
    return u'%s %s' %(info, list)

def info(bot):
    return ((u"s", u"ы"), 10, main)
