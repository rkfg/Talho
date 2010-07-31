# -*- coding: utf-8 -*-

import mpd
import base64
import urllib
import socket
import cookielib
import urllib2
import re
 
from misc import _

mpd_password = "mpdpassword" # set this to mpd pass
icecast_admin = ("admin", "adminpassword") # set this to admin pass
vk_acc = ("vk_login@vkontakte.ru", "vkontakte_password")

class IcecastAdminOpener(urllib.FancyURLopener):
    def prompt_user_passwd(self, host, realm):
        return icecast_admin

def shuffle(client, *args):
    client.random(1)
    client.next()
    
    return _("random started, next track is playing.")

def play(client, *args):
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
    for track in tracks:
        result += track["pos"] + ". "
        title = ""
        if "title" in track:
            title = track["title"]
            if "artist" in track:
                title = track["artist"] + " — " + title
        else:
            title = track["file"]
            
        result += title + "\n"
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
    result = client.playlistsearch("any", " ".join(args))
    return fancy_tracks(result)

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
        song_name = " ".join(args)
        metadata_opener = IcecastAdminOpener()
        update_query = urllib.urlencode({ "mount" : "/radio", "mode" : "updinfo", "song" : song_name.encode("utf-8") })
        metadata_opener.open("http://127.0.0.1:8000/admin/metadata?" + update_query).read()
        return _("new track name is '%s'.") % song_name
    except:
        return _("unknown fucking shit happened.")

def add_vk(client, *args):
    if not args:
        return

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    req = urllib2.Request("http://vkontakte.ru/login.php?email=%s&pass=%s" % vk_acc)
    handle = opener.open(req)
    req_args = urllib.urlencode({ "q" : " ".join(args).encode("utf-8"), "section" : "audio" })

    req = urllib2.Request("http://vkontakte.ru/gsearch.php?" + req_args)

    handle = opener.open(req)
    result = handle.read().decode("cp1251")

    match = re.search(ur"operate\((\d+),(\d+),(\d+),'([^']+)'", result)
    if match:
        link = "http://cs%s.vkontakte.ru/u%s/audio/%s.mp3" % (match.group(2), match.group(3), match.group(4))
        id = client.addid(link)
	client.playid(id)
        return _("found and started new track #%s") % id
    else:
        return _("nothing found.")
    
commands = { u'shuffle' : shuffle,
             u'sh' : shuffle,
	     u'ш': shuffle,
	     u'ыргааду': shuffle,
	     u'ыр': shuffle,
             u'p': play,
             u'play': play,
	     u'з': play,
	     u'здфн': play,
	     u'п': play,
             u'list': track_list,
             u'ls': track_list,
             u'l': track_list,
	     u'л': track_list,
	     u'дшые': track_list,
	     u'ды': track_list,
	     u'д': track_list,
             u'se': track_search,
             u'search': track_search,
	     u'с': track_search,
             u'ыу': track_search,
             u'ыуфкср': track_search,
             u'mounts': mounts_info,
             u'mi': mounts_info,
             u'ьщгтеы': mounts_info,
             u'ьш': mounts_info,
	     u'и': mounts_info,
	     u'м': mounts_info,
	     u'ми': mounts_info,
             u'tag': set_tag,
             u't': set_tag,
             u'ефп': set_tag,
             u'е': set_tag,
	     u'тег': set_tag,
	     u'т': set_tag,
	     u'v': add_vk,
	     u'в': add_vk
          }

def main(bot, args):
    '''Управление MPD. Команды:
shuffle, sh — включает режим рандомного проигрывания и пускает следующий трек
play, p <number> — запускает проигрывание трека номер <number> (0 — маунт first, 1 — маунт second, 2 - запись помех, далее рандомные треки)
list, ls, l [first] [last] — показывает список треков с [first] по [last]
se, search <query> — находит треки и выводит их с соответсвующими номерами (можно использовать для команды play)
mi, mounts — выдаёт список занятых диджейских маунтов, чтобы было проще определить свободный
t, tag <name> — установить название текущего трека в <name>
v, в <song and artist name> — ищет вконтактике и стартует указанную песню'''
    client = mpd.MPDClient()
    try:
        client.connect(host="127.0.0.1", port="6600")
    except SocketError:
        return "ошибка соединения!"
    try:
        client.password(mpd_password)
    except CommandError:
        client.disconnect()
        return "неверный пароль!"

    if args:
        cmd = args[0]
        if cmd in commands:
            try:
                result = commands[cmd](client, *args[1:])
	    except mpd.CommandError:
	        result = "Случилась неведомая ошибка во время выполнения команды."
	else:
	    result = _("unknown command")
    else:
        current_track = client.currentsong()
        if "pos" in current_track:
            result = _("now playing track #%s") % current_track["pos"].decode("utf-8")
        else:
            result = "ничего не проигрывается."
    client.disconnect()
    return result

if __name__ == "__main__":
	print main(None, None)
        
def info(bot):
    return ((u"mpd", u"m", u"ь", u"ьзв", u"м", u"мпд"), 9, main)

