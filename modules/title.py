import urllib2, re
from BeautifulSoup import BeautifulSoup

removetags=re.compile("<(.|\n)*?>")

def gettitle(url):
    response = urllib2.urlopen(url)
    data = response.read()
    soup = BeautifulSoup(data)
    result = unicode(soup.find("title"))
    return removetags.sub("",result)

def title(tbot, user, channel, msg):
    msg = msg.split(" ")
    for m in msg:
        if re.compile("^https?://.*").match(m):
            tbot.say(channel, "%s: %s" % (user, gettitle(m).encode("utf-8")))
title.rule = "^!title"
