def main(bot, args):
    '''lsmod\nShow loaded modules.\nSee also: load, modprobe, rmmod'''

    if not args:
        result = '\nlevel\tcommand\n'
        cmds = [(l[0], c) for (c, l) in bot.commands.items()]
        cmds.sort(reverse = True)
        for cmd in cmds:
            result += str(cmd[0]) + '\t\t' + cmd[1] + '\n'
        return result
    
def info(bot):
    return (("lsmod",), 10, main)

if __name__ == "__main__":
    print main(None, None)
