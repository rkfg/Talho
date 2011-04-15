# -*- coding: utf-8 -*-

import os
from misc import _

def main(bot, args):
    """сбросить кэш новостей."""
    try:
        os.unlink("/srv/radioanon.ru/htdocs/cache/cache.dat")
        os.unlink("/srv/radioanon.ru/htdocs/cache/cache.upd")
    except:
        pass
    return _("dropped cache.")
        
def info(bot):
    return ((u"news",), 1, main)

