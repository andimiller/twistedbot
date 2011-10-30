import urllib2
import json

def getCommitSummary(url):
    m = url.split("/")
    (username, reponame, ignoreme, changeset) = m[-4:]
    try:
        apiurl = "https://api.bitbucket.org/1.0/repositories/%s/%s/changesets/%s/" % (username, reponame, changeset)
        f = urllib2.urlopen(apiurl)
        data = f.read()
    except urllib2.HTTPError:
        return "Access Denied, repository is private."
    parseddata = json.loads(data)
    revision = parseddata["revision"]
    person = parseddata["author"]
    timestamp = parseddata["timestamp"]
    branch = parseddata["branch"]
    commitmessage = parseddata["message"]

    return "%s: [%s] %s - %s - %s" % (revision, timestamp, branch, person, commitmessage)


def bitbucket(tbot, user, channel, msg):
    m = msg.split(" ")
    tbot.msg(channel, '\x0311'+str(getCommitSummary(m[0])+chr(15)))
bitbucket.rule = "https://bitbucket.org/.*/changeset/.*"
