# -*- coding: utf-8 -*-

import SocketServer
import os, sys
import threading
import time
import radio
from xml.sax.saxutils import escape

botglobal = None

def netstat():
    result = []
    f = open("/proc/net/tcp", "r")
    for conn in f:
        connlist = conn.split()
        if "5F:1F40" in connlist[1] and connlist[3] == "01": # last ip octet:port is 5F:1F40
            hexip = connlist[2][:connlist[2].find(":")]
            decip = ".".join([str(int(hexip[x * 2] + hexip[x * 2 + 1], 16)) for x in xrange(len(hexip) / 2 - 1, -1, -1)])
            result.append(decip)

    f.close()
    return result

class MyUDHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global botglobal
        info = radio.getRadioState()[0]
        if botglobal.trackhurt["last_title"] != info:
            botglobal.trackhurt["last_title"] = info
            botglobal.trackhurt["voters"] = {}

        data = self.request[0]
        listeners = netstat()
        if ":" in data:
            ip, vote = data.rsplit(":", 2)
            if ip in listeners:
                if vote == "1" or vote == "0" or vote == "2":
                    if vote == "1":
                        botglobal.trackhurt["voters"][ip] = 1
                    elif vote == "0":
                        botglobal.trackhurt["voters"][ip] = -1
                    else:
                        if ip in botglobal.trackhurt["voters"]:
                            del botglobal.trackhurt["voters"][ip]

        level = 0
        for l, v in botglobal.trackhurt["voters"].items():
            if l in listeners:
                level += v

        if level < -(len(listeners) / 5) and len(botglobal.trackhurt["voters"]) > 2:
            botglobal.commands["mpd"][1](botglobal, ["sh"])

        thfile = open(botglobal.settings["th_file"], "w")
        thfile.write(str(level) + "/" + str(len(botglobal.trackhurt["voters"])))
        thfile.close()

class ThreadedUnixDatagramServer(SocketServer.ThreadingMixIn, SocketServer.UnixDatagramServer):
    pass
        
def info(bot):
    global botglobal
    botglobal = bot
    bot.trackhurt = {"last_title": "", "voters": {}}
    try:
        os.unlink("/tmp/thsock")
    except:
        pass

    if hasattr(bot, "thserver") and bot.thserver:
        bot.thserver.shutdown()
        bot.thserver = None
        time.sleep(2)

    server = ThreadedUnixDatagramServer("/tmp/thsock", MyUDHandler)
    os.chmod("/tmp/thsock", 0777)
    bot.thserver = server
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    return ((), 0, None)
