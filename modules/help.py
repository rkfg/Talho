def main(bot, args):
    '''help\nHelp.'''

    if not args:
        return 'Type %lsmod to show avialable modules.\nSources and bug tracker: http://kagami.touhou.ru/projects/show/cc'

def info(bot):
    return (("help",), 10, main)
