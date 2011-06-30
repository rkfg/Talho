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
        try:
            #result = handle.read().decode("cp1251")

            req = urllib2.Request("http://vkontakte.ru/search?c%%5Bq%%5D=%s&c%%5Bsection%%5D=audio" % self.path[1:])

            handle = opener.open(req)
            result = handle.read()
            handle.close()
            result = result.decode("cp1251", "ignore")

            match = re.search(ur"value=\"(http:[^,]+),", result)
            if match:
                link = match.group(1)
                mp3_handle = urllib2.urlopen(link)
	        self.send_response(200)
                self.send_header('Content-Type', mp3_handle.headers['Content-Type'])
                self.send_header('Content-Length', mp3_handle.headers['Content-Length'])
                self.end_headers()
	#tmpfile = open(dl_name, "wb")

                print "Transfer started"
                while True:
                    chunk = mp3_handle.read(128 * 1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
		    #tmpfile.write(chunk)

                print "Transfer finished"
		#tmpfile.close()
                mp3_handle.close()
		#tmpfile = open(dl_name, "rb")
                #while True:
                #    chunk = tmpfile.read(16 * 1024)
                #    if not chunk:
                #        break
                #    self.wfile.write(chunk)
		#tmpfile.close()
		self.wfile.close()
		#os.unlink(dl_name)
                return

	except socket.error, msg:
            print str("".join(traceback.format_exception(*sys.exc_info())))
	    #os.unlink(dl_name)
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

url = "http://vkontakte.ru/login.php?email=%s&pass=%s" % vk_acc
req = urllib2.Request(url)
handle = opener.open(req)
socket.setdefaulttimeout(15)

server = ThreadedHTTPServer(('0.0.0.0', 8080), VkHandler)
server.serve_forever()
