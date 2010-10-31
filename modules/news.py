# -*- coding: utf-8 -*-

import os
from misc import _

def main(bot, args):
    """сбросить кэш новостей."""
    try:
        os.unlink("/home/eurekafag/data/www/radioanon.ru/cache/cache.dat")
        os.unlink("/home/eurekafag/data/www/radioanon.ru/cache/cache.upd")
    except:
        pass
    return _("dropped cache.")
        
def info(bot):
    return ((u"news",), 1, main)

