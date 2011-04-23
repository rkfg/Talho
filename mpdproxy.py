#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mpd
import sys

client = mpd.MPDClient()
client.connect("127.0.0.1", "6600")
play = True
if sys.argv[1] == '!':
    play = False
    del sys.argv[1]
id = client.addid("http://127.0.0.1:8080/%s" % "+".join(sys.argv[1:]))
if play:
    client.playid(id)
