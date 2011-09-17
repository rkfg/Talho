#!/usr/bin/env python
# -*- coding: utf-8 -*-

def decoder(data):
    westeurcnt = 0
    cyrcnt = 0
    othercnt = 0
    #print [data]
    b = 0
    while b < len(data):
        if data[b] == "\xc2" or data[b] == "\xc3":
            westeurcnt += 1
            b += 2
        elif data[b] == "\xd0" or data[b] == "\xd1":
            cyrcnt += 1
            b += 2
        else:
            #print b, [data[b]]
            b += 1
            othercnt += 1

    #print westeurcnt, cyrcnt, othercnt, '/', len(data)
    data = data.decode("utf-8")
    #print len(data)
    if westeurcnt > cyrcnt and (othercnt / westeurcnt) < 1:
        try:
            data1252 = data.encode("cp1252")
        except UnicodeEncodeError:
            try:
                datalatin = data.encode("latin-1")
            except UnicodeEncodeError:
                return data

            return datalatin.decode("utf-8")
        data = data1252.decode("cp1251")
        return data
    else:
        return data

if __name__ == "__main__":
    print [decoder(u"Ìóìèé Òðîëëü — Äåëàé ìåíÿ òî÷íî".encode('utf-8'))]
    print [decoder(u"Ололошеньки-лоло".encode('utf-8'))]
    print [decoder(u"ÐÐ¸Ð½Ð¾ - ÐÑÑÐ¿Ð¿Ð° ÐºÑÐ¾Ð²Ð¸".encode('utf-8'))]
