# -*- coding: utf-8 -*-

import mpd
import base64
import urllib
import socket
import cookielib
import urllib2
import re
import datetime
import time
import HTMLParser
import traceback
import sys
from decoder import decoder

from misc import _

globalbot = None
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

def htmlunescape(s):
    p = HTMLParser.HTMLParser()
    return p.unescape(s)

class IcecastAdminOpener(urllib.FancyURLopener):
    def prompt_user_passwd(self, host, realm):
        global globalbot
        return globalbot.settings["icecast_admin"]

def check_block():
    global globalbot
    if "block_time" in globalbot.settings and datetime.datetime.now() < globalbot.settings["block_time"]:
        return _("mpd control is blocked, %s left") % (globalbot.settings["block_time"] - datetime.datetime.now())
    else:
        return None

def shuffle(client, *args):
    
    msg = check_block()
    if msg:
        return msg

    if len(args) > 0:
        if args[0] == 'off':
            client.random(0)
            return _("random was switched off.")
        if args[0] == 'on':
            client.random(1)
            return _("random was switched on.")
        if args[0] == 'st':
            return _("random is currently " + ("on" if client.status()["random"] == "1" else "off"))
    else:
        client.random(1)
        client.next()
    
        return _("random started, next track is playing.")

def play(client, *args):
    msg = check_block()
    if msg:
        return msg

    if len(args) != 1:
        return
    try:
        client.play(int(args[0]))
        if int(args[0]) < 3:
	    client.random(0)
        return _("track #%s started.") % args[0]
    except (ValueError, TypeError):
        return _("unknown fucking shit happened.")

def fancy_tracks(tracks):
    result = "\n"
    if not tracks:
        return _("nothing found.")
    try:
      for track in tracks:
        result += track["pos"] + ". "
        title = ""
        #if "title" in track:
        #    title = track["title"]
        #    if isinstance(title, list):
        #        title = " ".join(title)

        #    title = decoder(title)

        #    if "artist" in track:
        #        artist = track["artist"]
        #        if isinstance(artist, list):
        #            artist = " ".join(artist)
        #        artist = decoder(artist)

        #        title = artist + u" — " + title
        #else:
        title = track["file"].decode("utf-8")
            
        result += title + u"\n"
    except:
        print str("".join(traceback.format_exception(*sys.exc_info())))
    return result
    
def track_list(client, *args):
    playlist = client.playlistinfo()
    n = 3
    last = 10
    try:
        if len(args) == 1:
            n = int(args[0])
            last = n + 11
        elif len(args) == 2:
            n = int(args[0])
            last = int(args[1]) + 1
            if last <= n:
                return
            if last - n > 20:
                return _("too many items in query, maximum 20 allowed.")
            
    except ValueError:
        return
    return fancy_tracks(playlist[n:last])

def track_search(client, *args):
    if not args:
        return
    result = client.playlistsearch("any", (" ".join(args)).encode('utf-8'))[:20]
    return fancy_tracks(result)

def del_by_keyword(client, *args):
    name = " ".join(args)
    if len(name) < 4:
        return _("minimum 4 letters allowed")

    tracks = client.playlistsearch("any", name.encode('utf-8'))
    if not len(tracks):
        return _("nothing found.")

    trackstr = fancy_tracks(tracks)
    if len(trackstr) > 1000:
        trackstr = trackstr[:1000] + "..."
    cnt = 0
    for t in reversed(tracks):
        p = int(t["pos"])
        if p > 2:
            client.delete(p)
            cnt += 1

    return _("%d tracks deleted:%s") % (cnt, trackstr)

def group(client, *args):
    name = " ".join(args)
    if len(name) < 4:
        return _("minimum 4 letters allowed")

    tracks = client.playlistsearch("any", name.encode('utf-8'))
    if not len(tracks):
        return _("nothing found.")

    trackstr = fancy_tracks(tracks)
    if len(trackstr) > 1000:
        trackstr = trackstr[:1000] + "..."
    cnt = 0
    to = int(client.status()['playlistlength']) - 1
    for t in reversed(tracks):
        p = int(t["pos"])
        if p > 2:
            client.move(p, to)
            cnt += 1

    return _("%d tracks grouped at the end of playlist:%s") % (cnt, trackstr)

def mounts_info(client, *args):
    try:
        result = "\n"
        mounts_to_check = ( "/first", "/second" )
        admin_page_opener = IcecastAdminOpener()
        page = admin_page_opener.open("http://127.0.0.1:8000/admin/").read()
        for mount in mounts_to_check:
            if "<h3>Mount Point %s</h3>" % mount in page:
                result += "Маунт %s *занят*" % mount + "\n"
            else:
                result += "Маунт %s *свободен*" % mount + "\n"
                
        return result
    except:
        return _("unknown fucking shit happened.")

def set_tag(client, *args):
    if not args:
        return
    try:
        msg = check_block()
        if msg:
            return msg

        song_name = " ".join(args)[:100]
        metadata_opener = IcecastAdminOpener()
        update_query = urllib.urlencode({ "mount" : "/radio", "mode" : "updinfo", "song" : song_name.encode("utf-8") })
        metadata_opener.open("http://127.0.0.1:8000/admin/metadata?" + update_query).read()
        return _("new track name is '%s'.") % song_name
    except:
        return _("unknown fucking shit happened.")

def add_vk(client, *args):
    if not args:
        return

    try:
        global globalbot
        global opener
        aftercurrent = (args[0] == "!" and int(client.currentsong()["pos"]) > 1)
        if args[0] == "!":
            args = args[1:]

        req_args = urllib.urlencode({ "c[q]" : " ".join(args).encode('utf-8'), "c[section]" : "audio" })
        req = urllib2.Request("http://vkontakte.ru/search?" + req_args)

        handle = opener.open(req)
        result = handle.read().decode("cp1251")

        match = re.search(ur"value=\"(http:[^,]+),", result)
        if match:
            playtime = re.search(ur"<div class=\"duration fl_r\">([0-9:]+)</div>", result)
            id = client.addid(("http://127.0.0.1:8080/" + "+".join(args)).encode('utf-8'))
            if aftercurrent:
                client.move(int(client.status()['playlistlength']) - 1, int(client.currentsong()["pos"]) + 1)
	        position = int(client.currentsong()["pos"]) + 1
            else:
	        position = int(client.status()['playlistlength']) - 1
	    title = re.search(ur"<b><a href=[^>]+>([^<]+)</a></b> - <span id=\"title[^\"]+\">([^<]+)</span>", result)
	    if title:
	        title = title.group(1) + u" — " + title.group(2)
            else:
	        title = _("no title")

            if playtime:
                playtime = playtime.group(1)
                now = datetime.datetime.now()
            else:
                playtime = _("unknown")
                finish = _("unknown")

            return _("found new track #%s named \"%s\", duration is: %s") % (position, htmlunescape(title), playtime)
        else:
            return _("nothing found.")
    #except ValueError:
    except urllib2.URLError:
        return _("network error")

def delete_pos(client, *args):
    if not args:
        print "Need an argument"
    try:
        if int(args[0]) < 3:
	    return _("track is protected.")
        client.delete(int(args[0]))
        return _("removed track #%s from playlist") % args
    except:
        return _("FUCK YOU. I mean, error.")    

def set_next(client, *args):
    try:
        num = int(args[0])
	if num < 3:
	    return _("track is protected.")
	to = int(client.status()['playlistlength']) - 1
	client.move(num, to)
	return _("moved track #%d to #%d.") % (num, to)
    except:
        return

def last(client, *args):
    log = open("/home/dj/.mpd/mpd.log")
    tracks = []
    for line in log:
        if "playlist" in line:
            tracks.append(line)

    tracks = tracks[:-5]
    log.close()
    return "\n".join(tracks)

commands = { u'sh': shuffle,
             u'shuffle': shuffle,
	     u'ыр': shuffle,
	     u'ыргааду': shuffle,
	     u'рандом': shuffle,
	     u'хаос': shuffle,
             u'p': play,
             u'play': play,
	     u'з': play,
	     u'здфн': play,
	     u'играй': play,
	     u'поставь': play,
             u'l': track_list,
             u'ls': track_list,
             u'list': track_list,
	     u'д': track_list,
	     u'ды': track_list,
	     u'дшые': track_list,
	     u'покажи': track_list,
	     u'список': track_list,
             u's': track_search,
             u'se': track_search,
             u'search': track_search,
	     u'ы': track_search,
             u'ыу': track_search,
             u'ыуфкср': track_search,
             u'ищи': track_search,
             u'найди': track_search,
             u'm': mounts_info,
             u'mi': mounts_info,
	     u'mounts': mounts_info,
             u'ь': mounts_info,
             u'ьш': mounts_info,
	     u'ьщгтеы': mounts_info,
	     u'маунты': mounts_info,
             u't': set_tag,
             u'tag': set_tag,
             u'е': set_tag,
             u'ефп': set_tag,
             u'назови': set_tag,
	     u'v': add_vk,
	     u'м': add_vk,
	     u'запили': add_vk,
	     u'd': delete_pos,
	     u'в': delete_pos,
	     u'выпили': delete_pos,
	     u'n': set_next,
	     u'next': set_next,
	     u'т': set_next,
	     u'туче': set_next,
	     u'пни': set_next,
             u'dbk': del_by_keyword,
             u'вил': del_by_keyword,
             u'g': group,
             u'п': group
          }

def main(bot, args):
    '''Управление MPD. Команды:
shuffle, sh — включает режим рандомного проигрывания и пускает следующий трек.
*  sh off — отключает рандом, что даёт возможность набивать треки в очередь.
*  sh on — только включает рандом
*  sh st — сообщает статус рандома
play, p <number> — запускает проигрывание трека номер <number> (0 — маунт first, 1 — маунт second, далее рандомные треки)
list, ls, l [first] [last] — показывает список треков с [first] по [last]
search, se, s <query> — находит треки и выводит их с соответствующими номерами 
mounts, mi, m — показывает состояние диджейских маунтов
tag, t <name> — установить название текущего трека в <name>
v <song and artist name> — ищет вконтактике и добавляет указанную песню
d <number> — удаляет трек номер <number> (первые три защищены)
dbk <words> — удаляет треки по ключевому слову(ам)
next, n <number> — перемещает трек номер <number> в самый конец плейлиста
g <words> — группирует треки по ключевому слову(ам) в конце плейлиста
'''
    global globalbot
    globalbot = bot

    client = mpd.MPDClient()
    try:
        client.connect(**bot.settings["mpd_addr"])
    except socket.error, msg:
        return "ошибка соединения: " + msg
    try:
        client.password(bot.settings['mpd_password'])
    except mpd.CommandError:
        client.disconnect()
        return "неверный пароль!"

    if args:
        cmd = args[0]
        if cmd in commands:
            try:
                result = commands[cmd](client, *args[1:])
	    except mpd.CommandError:
	        result = _("unknown shit happend")
	else:
	    result = _("unknown command")
    else:
        current_track = client.currentsong()
        if "pos" in current_track:
            result = _("now playing track #%s") % current_track["pos"].decode("utf-8")
        else:
            result = _("playing nothing.")
    client.disconnect()
    return result

if __name__ == "__main__":
	print main(None, None)
        
def info(bot):
   req = urllib2.Request("http://vkontakte.ru/login.php?email=%s&pass=%s" % bot.settings['vk_acc'])
   handle = opener.open(req)

   return ((u"mpd", u"m", u"ь", u"ьзв", u"м", u"мпд"), 9, main)

