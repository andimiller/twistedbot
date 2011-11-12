def lastmsg(tbot, user, channel, msg):
    msg = msg.split()
    if len(msg)>1 and msg[1] in tbot.messages:
        tbot.msg(channel, "%s: I last saw %s say: %s" % (user, msg[1], tbot.messages[msg[1]]))
lastmsg.rule="^!lastmsg"

def storemessage(tbot, user, channel, msg):
    if not hasattr(tbot, "messages"):
        tbot.messages = dict()
    tbot.messages[user]=msg
storemessage.rule=".*"
