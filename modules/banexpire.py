from twisted.internet import protocol
from twisted.internet import task

def bandetect(tbot, user, channel, set, modes, args):
    nick = user.split("!")[0]
    if ("b" in modes) and (set==True):
        if nick in tbot.admins:
            tbot.say(channel, "You are the law.")
            return
        for index,b in enumerate(modes):
            tbot.logger.log("INFO", "Saw a ban by %s" % user)
            tbot.say(channel, "%s: Yo dawg, I pity the fool who thinks he an admin, I'll be removing that ban in 30 seconds." % nick)
            d = tbot.reactor.callLater(30, removeban, tbot, channel, args[index])
            #tbot.mode(channel, False, "-b %s" % args[index])
bandetect.modeChanged = True

def removeban(tbot, channel, ban):
    tbot.mode(channel, False, "-b %s" % ban)
