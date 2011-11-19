import re
import datetime

def sub(message, regex):
    regex=re.split("(?<!\\\\)/",regex)
    return re.sub(regex[1], regex[2], message)

def substitute(tbot, user, channel, msg):
    newmessage = sub(tbot.messages[user], msg)
    if newmessage != tbot.messages[user]:
        tbot.messages[user] = newmessage
        tbot.msg(channel, "<%s> %s" % (user, newmessage))
substitute.rule="^s\/.*"

def directedsubstitute(tbot, user, channel, msg):
    (target, regex) = re.compile("^(.*?): (.*)").match(msg).groups()
    newmessage = sub(tbot.messages[target], msg)
    if newmessage != tbot.messages[target]:
        tbot.messages[target] = newmessage
        tbot.msg(channel, "<%s> %s" % (user, newmessage))
directedsubstitute.rule="^.*?: s/.*"

def lastmsg(tbot, user, channel, msg):
    msg = msg.split()
    if len(msg)>1 and msg[1] in tbot.messages:
        tbot.msg(channel, "%s: I last saw %s say: %s" % (user, msg[1], tbot.messages[msg[1]]))
lastmsg.rule="^!lastmsg"

def seen(tbot, user, channel, msg):
    msg = msg.split()
    if len(msg)>1 and msg[1] in tbot.seen:
        tbot.msg(channel, tbot.seen[msg[1]])
seen.rule="^!seen"

def storemessage(tbot, user, channel, msg):
    if not hasattr(tbot, "seen"):
        tbot.seen = dict()
    if not hasattr(tbot, "messages"):
        tbot.messages = dict()
    if not msg.startswith("s/"):
        tbot.messages[user]=msg
    tbot.seen[user]= "I last saw %s at %s in %s. " % (user,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), channel)
storemessage.rule=".*"
