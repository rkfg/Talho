#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ReleaseFilter, ArtistIncludes, ReleaseIncludes
import musicbrainz2.model as m
from time import sleep
import codecs

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
sys.stdout = codecs.getwriter('utf8')(sys.stdout) # workaround for pipes

if len(sys.argv) < 2:
	print "Usage:", os.path.basename(sys.argv[0]), "'artist name' [offset]"
	sys.exit(1)

q = Query()

try:
	# Search for all artists matching the given name. Limit the results
	# to the 5 best matches. The offset parameter could be used to page
	# through the results.
	#
	f = ArtistFilter(name=sys.argv[1], limit=10)
	artistResults = q.getArtists(f)
except WebServiceError, e:
	print 'Error:', e
	sys.exit(1)

if len(sys.argv) > 2:
	artistResults = [artistResults[int(sys.argv[2])]]
else:
	artistResults = [artistResults[0]]
	
tracks_ids = []
for result in artistResults:
	artist_name = result.artist
	releases = []
	for rtype in [m.Release.TYPE_ALBUM, m.Release.TYPE_SINGLE, m.Release.TYPE_COMPILATION, m.Release.TYPE_REMIX]:
		artist = q.getArtistById(artist_name.id, ArtistIncludes(
				releases=(m.Release.TYPE_OFFICIAL, rtype),
				tags=True))
	
		releases.extend(artist.getReleases())

	for release in releases:
		sleep(1) # respect TOS
		release = q.getReleaseById(release.id, ReleaseIncludes(artist = True, tracks = True))
		for track in release.tracks:
			name = track.artist.name if track.artist else release.artist.name
			full_title = (name + u" — " + track.title).lower()
			if not full_title in tracks_ids:
				print name, track.title
				if not sys.stdout.isatty():
					print >> sys.stderr, full_title
				tracks_ids.append(full_title)
		sys.stdout.flush()
