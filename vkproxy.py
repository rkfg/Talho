#!/usr/bin/env python
# coding: utf-8

import sys
import time
import urllib, urllib2
import re
import traceback
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

vk_acc = ("bydlo@vkontakte.ru", "bydlopassword")

class VkHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

            req = urllib2.Request("http://vkontakte.ru/login.php?email=%s&pass=%s" % vk_acc)
            handle = opener.open(req)

            req = urllib2.Request("http://vkontakte.ru/gsearch.php?q=%s&section=audio" % self.path[1:])

            handle = opener.open(req)
            result = handle.read().decode("cp1251")
            handle.close()

            match = re.search(ur"onclick=\"return operate\((\d+),(\d+),(\d+),'([^']+)'", result)
            if match:
                link = "http://cs%s.vkontakte.ru/u%s/audio/%s.mp3" % (match.group(2), match.group(3), match.group(4))
                self.send_response(200)
                self.send_header('Content-type', 'audio/mp3')
                self.end_headers()
                mp3_handle = urllib2.urlopen(link)

                while True:
                    chunk = mp3_handle.read(16 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)

                mp3_handle.close()
                return
        except:
            print str("".join(traceback.format_exception(*sys.exc_info())))
            print '--------------------------------------------------------'
	    self.send_response(200)
	    return

        self.send_response(404)
        return

    def do_HEAD(self):
        self.send_response(200)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

server = ThreadedHTTPServer(('127.0.0.1', 8080), VkHandler)
server.serve_forever()
