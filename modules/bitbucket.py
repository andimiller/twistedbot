from BeautifulSoup import BeautifulSoup
import urllib2
import re
removetags=re.compile("<(.|\n)*?>")

def getCommitSummary(url):
    f = urllib2.urlopen(url)
    data = f.read()
    soup = BeautifulSoup(data)
    soup = soup.find("div", {"id" : "source-summary" })
    commitmessage = removetags.sub("",str(soup.find("p")))
    branch = removetags.sub("",str(soup.findAll("dd")[2]))
    person = removetags.sub("",str(soup.findAll("a")[-1]))
    return '\x0311'+"%s - %s - %s" % (person, branch, commitmessage) + chr(15)

def bitbucket(tbot, user, channel, msg):
    m = msg.split(" ")
    tbot.msg(channel, getCommitSummary(m[0]))
bitbucket.rule = "https://bitbucket.org/.*/changeset/.*"
