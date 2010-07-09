def main(bot, args):
    """exit (only for owner)\nExit."""

    if not args:
        bot.exit('EXIT: by request')

def info(bot):
    return (("exit",), 0, main)
