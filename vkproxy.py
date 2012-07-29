#!/usr/bin/env python
# coding: utf-8

import sys, os
import time
import urllib, urllib2
import re
import traceback
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import socket
from vkproxy_settings import vk_acc

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

class VkHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global opener

        dl_name = os.tmpnam()
        pathsplit = self.path[1:].split("/")
        songtitle = pathsplit[0]
        if len(pathsplit) > 1 and pathsplit[1].isdigit():
            songshift = int(pathsplit[1])
        else:
            songshift = 0

        try:
            req = urllib2.Request("http://vk.com/audio", data="act=search&al=1&gid=0&offset=0&sort=0&q=%s" % urllib.quote_plus(songtitle),
                                  headers={"X-Requested-With": "XMLHttpRequest", "Referer": "http://vk.com/audio?act=popular"})

            handle = opener.open(req)
            result = handle.read()
            handle.close()
            result = result.decode("cp1251", "ignore")

            match = re.findall(ur"value=\"(http:[^,]+),", result)
            if match:
                link = match[songshift]
                print "Link:", link
                mp3_handle = opener.open(link)
                
                self.send_response(200)
                self.send_header('Content-Type', mp3_handle.headers['Content-Type'])
                self.send_header('Content-Length', mp3_handle.headers['Content-Length'])
                self.end_headers()

                print "Transfer started"
                while True:
                    chunk = mp3_handle.read(128 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    
                print "Transfer finished"
                mp3_handle.close()
                self.wfile.close()
                return

        except socket.error, msg:
            print str("".join(traceback.format_exception(*sys.exc_info())))
            return
        except:
            print str("".join(traceback.format_exception(*sys.exc_info())))
            print '--------------------------------------------------------'
            self.send_response(404)
            return

        self.send_response(404)
        return

    def do_HEAD(self):
        self.send_response(200)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

url = "http://login.vk.com/?act=login"
req = urllib2.Request(url, data="email=%s&pass=%s" % vk_acc)
handle = opener.open(req)
handle.read()
handle.close()
print "Ready to serve."
socket.setdefaulttimeout(15)

server = ThreadedHTTPServer(('0.0.0.0', 8080), VkHandler)
server.serve_forever()
