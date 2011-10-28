import urllib2
import urllib

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
   print "gettitle called with:"+url
   f=urllib.urlopen(url)
   data=f.read()
   data=data.split("\n")
   message=""
   for line in data:
      if line.count("description") and line.count("<meta"):
         line=line.split("\"")
         message=message+line[1]
   return message

def tweetauto(tbot, user, channel, msg):
   data=msg
   url=data.split(" ")[0].replace("#!/", "")
   text=gettweet(url)
   text=unescape(text)
   tbot.msg(channel,text)
tweetauto.rule = r'^https?://twitter.com/'


if __name__ == '__main__': 
   print __doc__.strip()
