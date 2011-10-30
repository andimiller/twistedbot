import urllib2
import json

def getCommitSummary(url):
    m = url.split("/")
    (username, reponame, ignoreme, changeset) = m[-4:]
    apiurl = "https://api.bitbucket.org/1.0/repositories/%s/%s/changesets/%s/" % (username, reponame, changeset)
    f = urllib2.urlopen(apiurl)
    data = f.read()
    parseddata = json.loads(data)
    revision = parseddata["revision"]
    person = parseddata["author"]
    timestamp = parseddata["timestamp"]
    branch = parseddata["branch"]
    commitmessage = parseddata["message"]

    return '\x0311'+"%s: [%s] %s - %s - %s" % (revision, timestamp, branch, person, commitmessage) + chr(15)
print getCommitSummary("https://bitbucket.org/Sylnai/twistedbot/changeset/b3d833f49765")


def bitbucket(tbot, user, channel, msg):
    m = msg.split(" ")
    tbot.msg(channel, getCommitSummary(m[0]))
bitbucket.rule = "https://bitbucket.org/.*/changeset/.*"
