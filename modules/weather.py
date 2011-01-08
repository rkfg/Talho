# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
import xml.dom
import urllib, urllib2
from misc import _

def kmhtomsec(speed):
    try:
        speed = int(float(speed) * 1000.0 / 3600.0)
    except:
        speed = 0
    return str(speed)

def main(bot, args):
    '''Weather in the given city'''

    if not args:
        return
    
    city = " ".join(args).encode("utf-8")
    req_args = urllib.urlencode( { "where" : city } )
    handle = urllib2.urlopen("http://xoap.weather.com/search/search?" + req_args)
    response = parse(handle)
    loc = response.getElementsByTagName("loc")
    if loc:
        city = loc[0].attributes["id"].value
    else:
        return _("city not found.")

    handle = urllib2.urlopen("http://xoap.weather.com/weather/local/" + city + "?cc=*&unit=m&par=1121946239&key=3c4cd39ee5dec84f")
    try:
        response = parse(handle)
        cityname = response.getElementsByTagName("dnam")
        if not cityname:
            return _("city not found.")

	cityname = cityname[0].childNodes[0].nodeValue
	tags_cc = ( "lsup", "tmp", "t" )
	tags_wind = ( "s", "gust", "t" )
	cc = response.getElementsByTagName("cc")[0]
	for tag in tags_cc:
	    globals()["cc_" + tag] = cc.getElementsByTagName(tag)[0].childNodes[0].nodeValue

	wind = cc.getElementsByTagName("wind")[0]
	for tag in tags_wind:
	    globals()["wind_" + tag] = wind.getElementsByTagName(tag)[0].childNodes[0].nodeValue
	
	globals()["wind_s"] = kmhtomsec(globals()["wind_s"])
	if wind_gust != "N/A":
	    globals()["wind_s"] += "-" + kmhtomsec(globals()["wind_gust"])
    except IndexError:
        return _("error getting weather.")

    return _(u"weather for %s at %s: Temperature: %s°C, %s, Wind speed: %s m/sec, Wind direction: %s" ) % (cityname, cc_lsup.replace(" Local Time", ""), cc_tmp, cc_t, wind_s, wind_t)

    
def info(bot):
    return (("w", u"ц"), 10, main)
