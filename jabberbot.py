# -*- coding: utf-8 -*-

###############################################
# Based on JabberBot by Thomas Perl <thp@thpinfo.com>
# (http://thpinfo.com/2007/python-jabberbot/)
###############################################

import signal
import xmpp
import logging
import os
import re
import imp
import datetime
import time
import misc
import radio
import random
import traceback
import sys
import gettext
from xml.sax.saxutils import escape, unescape
from misc import _
import socket

class JabberBot:
    reconnectTime = 30

    def __init__(self, user, rooms, usersjid, usersnick, logfile): #{{{
        gettext.textdomain('talho')
        signal.signal(signal.SIGTERM, sigTermCB)
        signal.signal(signal.SIGHUP,  sigHupCB)

        self.jid = xmpp.JID(user[0])
        self.password = user[1]
        self.res = user[2]
        self.rooms = rooms
        self.usersnick = usersnick
        self.usersjid = usersjid
        self.conn = None
        self.__finished = False

        self.iq = True
        self.info = ''
        self.last = datetime.datetime(1, 1, 1)
        self.plaintext_dispatchers = {}

        socket.setdefaulttimeout(15)

        logging.basicConfig(level=logging.DEBUG, filename=logfile, format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    #}}}

    ###############################################

    def load(self, bot=None, args=None): #{{{
        '''load\nLoad all modules.\nSee also: modprobe, rmmod, lsmod'''

        if args: return
        self.commands = {'load': (0, self.load), 'modprobe': (0, self.modprobe), 'rmmod': (0, self.rmmod)}
        for file in os.listdir('modules'):
            if file.endswith('.py'):
                self.modprobe(self, [file[:-3]])
                
        return 'done'
    #}}}

    def modprobe(self, bot, args): #{{{
        '''modprobe <module>\nLoads module.\nSee also: load, rmmod, lsmod'''

        if len(args) != 1: return

        try:
            file, pathname, description = imp.find_module("modules/" + args[0])
            name = "modules/" + args[0]
        except:
            error = _('MODULE: %s not found') % args[0]
            logging.error(error)
            return error

        try:
            method = imp.load_module(name, file, pathname, description).info
        except:
            error = _('MODULE: can\'t load %s') % args[0]
            logging.error(error)
            return error
        else:
            info = method(bot)
            if info[0] == '':
                self.plaintext_dispatchers[args[0]] = info[1:]
            else:
                for command in info[0]:
                    self.commands[command] = info[1:]

        info = _('MODULE: %s loaded') % args[0]
        logging.info(info)
        return info
    #}}}

    def rmmod(self, bot, args): #{{{
        '''rmmod <module>\nRemove module.\nSee also: load, modprobe, lsmod'''

        if len(args) != 1: return

        if args[0] == 'load' or args[0] == 'modprobe' or args[0] == 'rmmod':
            return _('MODULE: can\'t remove %s') % args[0]

        if self.commands.has_key(args[0]):
            del self.commands[args[0]]
        else:
            return _('MODULE: %s not loaded') % args[0]

        info = _('MODULE: %s removed') % args[0]
        logging.info(info)
        return info
    #}}}

    ###############################################

    def connect(self): #{{{
        if not self.conn:
            #conn = xmpp.Client(self.jid.getDomain(), debug = ['always', 'nodebuilder'])
            conn = xmpp.Client(self.jid.getDomain(), debug = [])

            if not conn.connect():
                logging.error('CONNECTION: unable to connect to server')
                return

            if not conn.auth(self.jid.getNode(), self.password, self.res):
                logging.error('CONNECTION: unable to authorize with server')
                return

            for room, data in self.rooms.iteritems():
                self._join_presence(conn, room, data[0])

            conn.RegisterHandler('message', self.messageCB)
            conn.RegisterHandler('presence', self.presenceCB)
            conn.RegisterHandler('iq', self.iqCB, typ='result', ns=xmpp.NS_TIME)
            conn.sendInitPresence()

            self.conn = conn
            return True
    #}}}

    def exit(self, msg = 'exit'): #{{{
        if self.conn:
            for room, data in self.rooms.iteritems():
                self.leave(room)
            self.conn = None

        self.__finished = True
        logging.info(msg)
    #}}}

    def _validate(self, text): #{{{
        return escape(unescape(text, {'&quot;': '\'', '&#39;': '\'', '&#44;': ',', '&middot;': u'·'}))
    #}}}

    def send(self, user, type, text, extra = ''): #{{{
        self.conn.send(u'<message to="%s" type="%s"><body>%s</body>%s</message>' %(user, type, self._validate(text), extra))
    #}}}

    def _join_presence(self, conn, room, password=None): #{{{
        if password:
            conn.send('<presence to=\'%s/%s\'><x xmlns=\'http://jabber.org/protocol/muc\'><password>%s</password></x></presence>'
                      %(room, self.res, password))
        else:
            conn.send(xmpp.Presence(to='%s/%s' %(room, self.res)))
    #}}}

    def join(self, room): #{{{
        if not room[0] in self.rooms:
            self._join_presence(self.conn, room[0], room[1])
            self.rooms[room[0]] = (room[1], room[2])
            return True
    #}}}

    def leave(self, room): #{{{
        if room[0] in self.rooms:
            self.conn.send(xmpp.Presence(to='%s/%s' %(room[0], self.res), typ='unavailable', status='offline'))
            del self.rooms[room[0]]
            return True
    #}}}

    def _inRoom(self, user): #{{{
        return user in self.rooms
    #}}}

    def messageCB(self, conn, mess): #{{{
        # Just a history
        if mess.getTimestamp():
            return

        type = mess.getType()
        mfrm = mess.getFrom()
        user = mfrm.getStripped()
        prefix = mfrm.getResource()
        if type != 'groupchat':
            #logging.info(misc.force_unicode(user) + " " + misc.force_unicode(prefix) + " " + misc.force_unicode(mess.getBody()))
            return 

        if (not prefix) or (type == 'groupchat' and prefix == self.res):
            return

        text = misc.force_unicode(mess.getBody())

        level = 10
        if self._inRoom(user):
            if prefix == "Miria":
                return
            level = self.rooms[user][1] # room-level
            if prefix in self.usersnick:     # Msg from room
                level = self.usersnick[prefix]
        else:
            if user in self.usersjid:     # Msg from jid
                level = self.usersjid[user]

        # Checking command
        if text:
            if text[0] == '%':
                text = text[1:]
            elif type == 'groupchat':
                for dispatcher in self.plaintext_dispatchers:
                    result = self.plaintext_dispatchers[dispatcher][0] >= level and self.plaintext_dispatchers[dispatcher][1](self, text)
                    if result:
                        self.send(user, type, misc.force_unicode(prefix) + u", " + misc.force_unicode(result))
                        return
                                     
                if not text.startswith('%show') and re.search('http://[^ ]+', text):
                    link = re.findall('(http://[^ ]+)', text)[0]
                    title = misc.getTitle(link, self)
                    if title:
                        if re.search('http://(www\.)?youtube.com/', link) and re.search('[rR][iI][cC][kK]', title):
                            self.send(user, type, u'%s — там рикролл!!!' %link)
                        else:
                            tiny = ''
                            if len(link) > 70: tiny = ' ( %s )' %misc.makeTiny(link, self)
                            self.send(user, type, u'Title: %s%s' %(title, tiny))
                return
            else:
                return
        else:
            return

        # Parsing command
        spl = text.split()
        if spl:
            cmd, args = spl[0].lower(), spl[1:]
        else:
            return

        if type == 'groupchat':
            if '>' in args:
                index  = args.index('>')        # Redirect (>)
                prefix = ''
                redir  = ' '.join(args[index+1:])
                if redir:
                    prefix = redir + ', '
                args = args[:index]
            else:
                prefix += ', '                  # Groupchat => prefix
        else:
            user, prefix = mfrm, ''             # Chat => no prefix

        # Executing command
        error = None
        if self.commands.has_key(cmd):
            if self.commands[cmd][0] >= level:
                try:
                    result = self.commands[cmd][1](self, args)
                except:
                    error = True
            else:
                result = 'доступ запрещён. Вам нужен минимум уровень %d, но у вас %d' % (self.commands[cmd][0], level)
        else:
            return #result = 'command not found: %s' %(cmd)

        if self.__finished: return

        if error:
            error = u'Исключение в модуле %s. Трейсбэк: %s' % (cmd, str("".join(traceback.format_exception(*sys.exc_info()))))
            logging.error(error)
            msg, extra = error, ''
        else:
            if result:
                if isinstance(result, tuple):
                    msg, extra = result
                else:
                    msg, extra = result, ''
            else:
                msg, extra = 'синтаксическая ошибка.', ''

        # Replying
        if msg:
            self.send(user, type, prefix + misc.force_unicode(msg), extra)
    #}}}

    def presenceCB(self, conn, pres): #{{{
        if pres.getType() == 'subscribe' and pres.getFrom().getStripped() in self.usersjid:
            self.conn.send(xmpp.Presence(to=pres.getFrom(), typ='subscribed'))

        if pres.getFrom().getResource() == self.res and pres.getType() == 'unavailable' and pres.getStatus() == 'Replaced by new connection':
            user = pres.getFrom().getStripped()
            for room, data in self.rooms.iteritems():
                if user == room:
                    self._join_presence(self.conn, room, data[0])
    #}}}

    def iqCB(self, conn, iq_node): #{{{
        self.iq = iq_node
    #}}}

    def process(self): #{{{
        while not self.__finished:
            try:
                self.checkReconnect()

                if self.conn:
                    if self.conn.Process(1) == 0:
                        self.connect()
                else:
                    if self.connect():
                        logging.info('CONNECTION: bot connected')
                    else:
                        time.sleep(self.reconnectTime)
            except xmpp.protocol.XMLNotWellFormed:
                logging.error('CONNECTION: reconnect (detected not valid XML)')
                self.conn = None
            except KeyboardInterrupt:
                self.exit('EXIT: interrupted by keyboard')
            except SystemExit:
                self.exit('EXIT: interrupted by SIGTERM')
            except ReloadData:
                logging.info('RELOAD: by SIGHUP')
                self.load()
            except:
                pass
    #}}}

    def checkReconnect(self): #{{{
        return
        if self.conn:
            now = datetime.datetime.now()
            if (now - self.last).seconds > self.reconnectTime:
                if self.iq:
                    self.iq = None
                self.last = now
                self.conn.send(xmpp.protocol.Iq(to='jabber.ru', typ='get', queryNS=xmpp.NS_TIME))
            else:
                logging.warning('CONNECTION: reconnect (iq reply timeout)')
                self.conn = None
                self.iq = True
    #}}}

###############################################

def sigTermCB(signum, frame): #{{{
    raise SystemExit()
#}}}

class ReloadData(Exception): #{{{
    pass
#}}}

def sigHupCB(signum, frame): #{{{
    raise ReloadData()
#}}}
