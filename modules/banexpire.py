from twisted.internet import protocol
from random import choice
from twisted.internet import task

banresponses = [
        "Yo dawg, I pity the fool who thinks they be an admin. Your ban will be removed in 30 seconds.",
        "Stop right there criminal scum. Your ban will be removed in 30 seconds.",
        "I used to make bans like you, but then I took an arrow to the... face. As will you in 30 seconds.",
        "I see what you did there, and I'll be reverting it in 30 seconds."
        ]


def bandetect(tbot, user, channel, set, modes, args):
    nick = user.split("!")[0]
    if ("b" in modes) and (set==True):
        if nick in tbot.admins:
            tbot.say(channel, "You are the law.")
            return
        for index,b in enumerate(modes):
            tbot.logger.log("INFO", "Saw a ban by %s" % user)
            tbot.say(channel, "%s: %s" % (nick,choice(banresponses)))
            d = tbot.reactor.callLater(30, removeban, tbot, channel, args[index])
            #tbot.mode(channel, False, "-b %s" % args[index])
bandetect.modeChanged = True

def removeban(tbot, channel, ban):
    tbot.mode(channel, False, "-b %s" % ban)
