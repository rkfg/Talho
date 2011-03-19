# -*- coding: utf-8 -*-

import datetime

from misc import _

def main(bot, args):
    """блокировка управления mpd на указанное число минут"""

    if not len(args):
       if not "block_time" in bot.settings or bot.settings["block_time"] < datetime.datetime.now():
           return _("mpd isn't blocked.")
       return _("%s left.") % (bot.settings["block_time"] - datetime.datetime.now())

    try:
        block_time = int(args[0])
    except ValueError:
        return

    if block_time < 0 or block_time > 60:
        return

    if block_time == 0:
        bot.settings["block_time"] = datetime.datetime.now()
	return _("block was reset.")

    bot.settings["block_time"] = datetime.datetime.now() + datetime.timedelta(minutes = block_time)
    return _("block time was set to %d minutes.") % block_time

def info(bot):
    return ((u"block", u"блок"), 2, main)


