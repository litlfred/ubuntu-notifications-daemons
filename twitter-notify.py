#!/usr/bin/env python


import twitter
import time
import pynotify
from urllib import urlretrieve
import tempfile
import os

wait=15 #default is 15 seconds but can be overridden in config.py
execfile(os.path.expanduser("~/.twitternotify/config.py"))


################################################################################
##
## Info: 
##    Python Twitter notifications daemon for ubuntu notifyosd
## 
## Dependencies:
##    python-twitter
##       source is found here:  http://code.google.com/p/python-twitter/
##       the currently available package for ubuntu (0.6) does not support oAuth. see the bug:
##          https://bugs.launchpad.net/ubuntu/+source/python-twitter/+bug/746850
##       and indicate that it affects you.  in the meantime you can do:
##           hg clone http://python-twitter.googlecode.com/hg/ python-twitter
##	     cd python-twitter
##	     hg update
##           python setup.py build
##	     sudo python setup.py install
##       once the above bug is resolved you will be able to do instead:
##           apt-get install python-twitter)
##
##Configure:
##    see config.py for instructions
##
## Run:
##    python twitter-notify.py 
##			(from Run prompt or Session/start-up programs)
##		python twitter-notify.py & 
##			(from command line. just don't close out the terminal window)
##
##			actual daemon will happen soon enough
##
## Copyright 2009 James Wilson, 2012 Carl Leitner
##
## Author:
##    James Wilson <j@meswilson.com>
##    http://ja.meswilson.com/blog/
##
## 
##    Carl Leitner <litlfred@ibiblio.org>
##    https://github.com/litlfred
##
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License version 3, as published
## by the Free Software Foundation.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranties of
## MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
## PURPOSE.  See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program.  If not, see <http://www.gnu.org/licenses/>.
##
################################################################################



if not pynotify.init ("icon-summary-body"):
	sys.exit(1)

api = 0
def login():
	global api,c_key,c_secret,a_key,a_secret
	try:
		api = twitter.Api(consumer_key=c_key, consumer_secret=c_secret, access_token_key=a_key, access_token_secret=a_secret)
	except:
		time.sleep(15)
		return login()
login()

all = []
icons = {}

def geticon(url):
	global icons
	if url in icons.viewkeys():
		file = icons[url]
	else:
		f = tempfile.NamedTemporaryFile()
		f.close()
		file = f.name
		urlretrieve(url,file)
		icons[url] = file
	return file


def notify(user,message):
	n = pynotify.Notification (user.screen_name,message,geticon(user.profile_image_url))
	n.show()

while 1:
	try:	
		stat = api.GetFriendsTimeline(count=5)
		
	except:
		time.sleep(wait)
		login()
	else:
		if len(all) == 0 and backlog == 0:
			for s in stat:
				all.append(s.text)
		for s in stat:
			if not s.text in all:
				notify(s.user,s.text)
				all.append(s.text)

		time.sleep(wait)

