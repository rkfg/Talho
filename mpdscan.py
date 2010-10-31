#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mpd
import httplib
import urllib

mpd_password = "mpdpassword"

client = mpd.MPDClient()
try:
    client.connect(host="127.0.0.1", port="6600")
except mpd.SocketError:
    print "ошибка соединения!"
    raise SystemExit

if mpd_password:
    try:
        client.password(mpd_password)
    except mpd.CommandError:
        client.disconnect()
        print "неверный пароль!"
        raise SystemExit

track_count = int(client.status()['playlistlength'])

info = client.playlistinfo()
for track in info:
    if track['file'].startswith('http://cs'):
        host, path = urllib.splithost(track['file'][5:])
        c = httplib.HTTPConnection(host)
        c.request('HEAD', path)
        r = c.getresponse()
        if str(r.status)[0] != '2':
            #print "%s expired [%d], deleting..." % (track['file'], r.status)
            client.deleteid(track['id'])
