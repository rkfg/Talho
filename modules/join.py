# -*- coding: utf-8 -*-

from misc import _

def main(bot, args):
    """join <room> [pass]\nJoin a room.\nSee also: leave, rooms"""

    room = [ '', '', 10 ]
    room[:len(args)] = args
    room[2] = int(room[2])
    if not room[0]:
        return

    if bot.join(room):
        return _('done.')
    else:
        return _('I\'m already in this room.')

def info(bot):
    return (("join",), 0, main)
