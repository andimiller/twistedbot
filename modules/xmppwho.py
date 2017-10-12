#!/usr/bin/env python
from __future__ import print_function

import urllib
import re
import requests
import eveapi
import arrow
from dateutil.parser import parse

NORMAL = u""
RED = u""
GREEN = u""
YELLOW = u""
ORANGE = u""

def formatsecstatus(data):
	data = "%.2f" % data
	value = float(data)
	if value < -5:
		return (RED, data)
	if value < 0:
		return (ORANGE, data)
	if value <= 4:
		return (NORMAL, data)
	if value > 4:
		return (GREEN, data)


def last_active(i):
	try:
		r = requests.get("https://zkillboard.com/api/characterID/%d/page/1/" % i, verify=False, timeout=10).json()
		return arrow.get(parse(r[0]["killmail_time"])).humanize()
	except Exception as e:
		return "NEVER BEEN ACTIVE"

def getdetailshash(name):
	api = eveapi.EVEAPIConnection()
	r = api.eve.CharacterID(names=name).characters
	assert(len(r)>0)
	id = r[0].characterID
	r = api.eve.CharacterInfo(characterID=id)
	return (id, r)

def getkbstats(id):
	ZKBAPI = "https://zkillboard.com/api/stats/characterID/%s/"
	EVEKILLAPI = "https://beta.eve-kill.net/api/stats/characterID/%d/"
	r = requests.get(ZKBAPI % id, timeout=10)
	data = r.json()
	#kills = data["totals"]["countDestroyed"]
	#lost = data["totals"]["countLost"]
	kills = data["shipsDestroyed"]
	lost = data["shipsLost"]
	try:
		trophies = data["trophies"]["levels"]
		trophiestotal = data["trophies"]["max"]
		trophiestext = "("+str(trophies)+"/"+str(trophiestotal)+")"
	except Exception as e:
		trophiestext = ""
	return "["+GREEN+str(kills)+NORMAL+", "+RED+str(lost)+NORMAL+"]"+trophiestext

def who(tbot, user, channel, msg):
	target = msg.replace("!who ", "")
	id, r = getdetailshash(target.strip())
	if hasattr(r, "securityStatus"):
		sec = formatsecstatus(r.securityStatus)
	else:
		sec = ("", "")
	try:
		kbstats = getkbstats(id)
	except Exception as e:
		kbstats = "[NOKILLBOARD]"

	created = arrow.get(r.employmentHistory[-1].startDate).humanize()
	startDate = arrow.get(r.employmentHistory[0].startDate).humanize()

	if not hasattr(r, "alliance"):
		tbot.say(channel, "%s%s %s%s%s%s {%s} - %s (%s)" %  (sec[0], r.characterName, "["+sec[1]+"]", NORMAL, kbstats, "(last active "+last_active(id)+")", created, r.corporation, startDate))
	else:
		message = "%s%s %s%s%s%s {%s} - %s (%s) - %s" % (sec[0], r.characterName, "["+sec[1]+"]", NORMAL, kbstats, "(last active "+last_active(id)+")", created, r.corporation, startDate, r.alliance)
		tbot.say(channel, message)
who.rule="^!who "

if __name__ == "__main__":
	a = lambda x:x
	a.say = print
	who(a, None, None, "!who Lucia Denniard")
