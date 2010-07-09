# -*- coding: utf-8 -*-

from misc import _

def main(bot, args):
    """leave <room> [pass]\nПокинуть комнату <room>.\nСм. также: join, rooms"""

    if len(args) == 1: room = (args[0], '')
    elif len(args) == 2: room = (args[0], args[1])
    else: return

    if bot.leave(room):
        return _('done.')
    else:
        return _('I\'m not in that room.')

def info(bot):
    return (("leave",), 0, main)
