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
from vkproxy_settings import vk_acc, vk_max_res

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
resolutions = [240, 360, 480, 720]

class VkHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global opener

        dl_name = os.tmpnam()
        try:
            #result = handle.read().decode("cp1251")

            searchlink = "http://vkontakte.ru/search?section=video&" + urllib.urlencode({'q':  urllib.unquote(self.path[1:]).decode('utf-8').encode('cp1251')}) # WOK
            req = urllib2.Request(searchlink)

            handle = opener.open(req)
            result = handle.read()
            handle.close()

            matches = re.findall(ur"onclick=\"return showVideo\('([^']+)',", result)
            for match in matches: # iterate vids and play first that from vkontakte
                data = 'video=' + match + '&act=show&al=1&autoplay=0'
                req  = urllib2.Request("http://vkontakte.ru/al_video.php", data)
                handle = opener.open(req)
                videopage = handle.read().decode("cp1251")
                handle.close()
                idsmatch = re.search(ur'"uid":"([^"]+)","vid":"[^"]+","oid":"[^"]+","host":"([^"]+)","vtag":"([^"]+)","ltag":"[^"]+","vkid":"([^"]+)"', videopage)
                if idsmatch:
                    if idsmatch.group(2).startswith("http:"):
                        host = idsmatch.group(2).replace("\\", "") # old vk
                        if videopage.find('"no_flv":1') > 0: # mp4, get the highest definition
                            vresm = re.search(ur'"hd":(\d)', videopage)
                            if vresm:
                                if int(vresm.group(1)) > vk_max_res:
                                    vres = resolutions[vk_max_res]
                                else:
                                    vres = resolutions[int(vresm.group(1))]
                            else:
                                vres = 240
                            ext = str(vres) + '.mp4'
                        else:
                            ext = 'flv'
                        link = "%su%s/video/%s.%s" % (host, idsmatch.group(1), idsmatch.group(3), ext)
                    else:
                        link = "http://%s/assets/videos/%s%s.vk.flv" % (idsmatch.group(2), idsmatch.group(3), idsmatch.group(4))
                        
                    print "Direct link:", link
                    flv_handle = urllib2.urlopen(link)
                    self.send_response(200)
                    self.send_header('Content-Type', flv_handle.headers['Content-Type'])
                    self.send_header('Content-Length', flv_handle.headers['Content-Length'])
                    self.end_headers()

                    while True:
                        chunk = flv_handle.read(128 * 1024)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                    flv_handle.close()
                    self.wfile.close()
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

server = ThreadedHTTPServer(('0.0.0.0', 8081), VkHandler)
server.serve_forever()
