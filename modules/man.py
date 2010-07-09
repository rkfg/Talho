# -*- coding: utf-8 -*-

def main(bot, args):
    """man [page]\nShow manual page.\nSee also: help"""

    if not args:
        return 'What manual page do you want?'
    elif len(args) == 1:
        man = ''
        if bot.commands.has_key(args[0]):
            man = bot.commands[args[0]][1].__doc__

        if man:
            return man
        else:
            return 'No manual entry for %s' %(args[0])

def info(bot):
    return (("man",), 10, main)
