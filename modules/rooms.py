def main(bot, args):
    """rooms (only for owner)\nList rooms.\nSee also: join, leave"""

    if args: return

    if not bot.rooms:
        return 'None'
    else:
        rooms_list = u''
        for room in bot.rooms:
            rooms_list += u'\n%s %s' %(room, bot.rooms[room][0])
        return rooms_list

def info(bot):
    return (("rooms",), 0, main)
