# -*- coding: utf-8 -*-

import urllib
from HTMLParser import HTMLParser

wanted_streams = ['/radio', '/radio-low']
html_ents = {'amp': '&', 'nbsp': ' ', 'lt': '<', 'gt': '>'}

S_GOTO_MOUNTPOINT = 0
S_GET_MP_NAME = 1
S_GOTO_ATTRS = 2
S_NEXT_ATTR = 3
S_TO_ATTR_NAME = 4
S_GET_ATTR_NAME = 5
S_TO_ATTR_VALUE = 6
S_GET_ATTR_VALUE = 7

class jbStream:
    def __init__(self):
        self.dj, self.title = "", ""
        self.current, self.peak = 0, 0
    def __str__(self):
        return "%s <- dj %s (%d/%d)" % (self.title,self.dj,self.current,self.peak)
    def __repr__(self):
        return '"' + self.__str__() + '"'
    def setAttribute(self,name,value):
        if name.startswith("Stream Description"):
            self.dj = value
        elif name.startswith("Current Listeners"):
            self.current = int(value)
        elif name.startswith("Peak Listeners"):
            self.peak = int(value)
        elif name.startswith("Current Song"):
            self.title = value

class jbHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.state = S_GOTO_MOUNTPOINT
        self.stm = dict()
        self.cur_stm = ''
        self.attr_name = ''
        self.attr_value = ''

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.state = S_GET_MP_NAME
        elif self.state == S_GOTO_ATTRS and tag == "table":
            self.state = S_NEXT_ATTR
        elif tag == "tr" and self.state >= S_NEXT_ATTR:
            self.state = S_TO_ATTR_NAME
        elif self.state == S_TO_ATTR_NAME and tag == "td":
            self.state = S_GET_ATTR_NAME
        elif self.state == S_TO_ATTR_VALUE and tag == "td":
            self.state = S_GET_ATTR_VALUE

    def handle_endtag(self, tag):
        if self.state == S_GET_ATTR_VALUE and tag == "td":
            self.stm[self.cur_stm].setAttribute(self.attr_name,self.attr_value)
            self.state = S_NEXT_ATTR

    def handle_entityref(self, ref):
        if self.state == S_GET_ATTR_VALUE:
            self.attr_value += html_ents[ref]

    def handle_data(self, data):
        if self.state == S_GET_MP_NAME and data.startswith("Mount Point"):
            if data[12:] in wanted_streams:
                self.state = S_GOTO_ATTRS
                self.cur_stm = data[12:]
                self.stm[self.cur_stm] = jbStream()
            else:
                self.state = S_GOTO_MOUNTPOINT
        elif self.state == S_GET_ATTR_NAME:
            self.state = S_TO_ATTR_VALUE
            self.attr_name = data
            self.attr_value = ""
        elif self.state == S_GET_ATTR_VALUE:
            self.attr_value += data
			
def getRadioState(radiourl='http://127.0.0.1:8000'):
	try:
		page = urllib.urlopen(radiourl)
		data = page.read()
	except:
		return "can't get page", ""
	try:
		parser = jbHTMLParser()
		parser.feed(data)
		parser.close()
		stm_main = parser.stm['/radio']
		stm_low = parser.stm['/radio-low']

		info = u'%s ⇐ %s' %(unicode(stm_main.title, 'utf-8'), unicode(stm_main.dj, 'utf-8'))
		list = u'(%d+%d/%d+%d)' %(stm_main.current, stm_low.current, stm_main.peak, stm_low.peak)
		return info, list
	except:
		return "can't parse data", ""
