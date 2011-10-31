import urllib2
import json

def getCommitSummary(username, reponame, changeset):
    try:
        apiurl = "https://api.bitbucket.org/1.0/repositories/%s/%s/changesets/%s/" % (username, reponame, changeset)
        f = urllib2.urlopen(apiurl)
        data = f.read()
    except urllib2.HTTPError:
        return "Access Denied, repository is private."
    data = json.loads(data)
    revision = data["revision"]
    person = data["author"]
    timestamp = data["timestamp"]
    branch = data["branch"]
    commitmessage = data["message"]

    return "%s: [%s] %s - %s - %s" % (revision, timestamp, branch, person, commitmessage)

def getAllCommits(repo):
    (username, reponame, lastcommit) = repo
    url = "https://api.bitbucket.org/1.0/repositories/%s/%s/changesets" % (username, reponame)
    while True:
        f = urllib2.urlopen(url)
        data = f.read()
        data = json.loads(data)
        revisions = data["changesets"]
        revisions = filter(lambda x:x["revision"] > lastcommit, revisions)
        if len(revisions)==0:
            yield False
        for k in revisions:
            if k["revision"] > lastcommit:
                lastcommit = k["revision"]
                yield getCommitSummary(username, reponame, k["node"])

def watchIt(tbot):
    channel = "#lolhax"
    for i, repo in enumerate(tbot.repos):
        generator = getAllCommits(repo)
        d=generator.next()
        tbot.logger.log("INFO", str(d))
        if d != False:
            tbot.msg(channel, str(d)) #'\x0311'+d+chr(15)_)
            tbot.repos[i][2] += 1
        else:
            tbot.say(channel, "No new changes in %s/%s after revision %d" % (repo[0], repo[1], repo[2]))
watchIt.main = True
