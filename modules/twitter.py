import urllib2
import urllib
import json

import re, htmlentitydefs

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def gettweet(url):
    print "gettitle called with: " + url
    tweet_id =  re.match(tweetauto.rule, url).groups()[-1]
    api_url = "https://api.twitter.com/1/statuses/show/%s.json" % tweet_id
    f = urllib.urlopen(api_url)
    data = f.read()
    data = json.loads(data)
    return data["text"]

def tweetauto(tbot, user, channel, msg):
    data=msg
    url=data.split(" ")[0].replace("#!/", "")
    text=gettweet(url)
    text=unescape(text)
    tbot.msg(channel,text.encode("utf-8"))
tweetauto.rule = r'^https?://(www.)?twitter.com/\w+/status/([0-9]+)'


if __name__ == '__main__':
    tweet_url = "https://twitter.com/MrBrownstone_/status/4507596236"
    print gettweet(tweet_url)
