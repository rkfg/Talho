# -*- coding: utf-8 -*-

import datetime

def main(bot, args):
    '''date\nShow current date and time.'''

    if not args:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def info(bot):
    return (("date", u"дата"), 10, main)
