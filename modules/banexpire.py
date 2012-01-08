from twisted.internet import protocol
from random import choice
from twisted.internet import task

banresponses = [
        "Yo dawg, I pity the fool who thinks they be an admin.",
        "Stop right there criminal scum.",
        "I used to make bans like you, but then I took an arrow to the...",
        "I see what you did there.",
        "It would appear that love and tolerance are lost arts.",
        "Remember, don't feed the trolls.."
        ]


def bandetect(tbot, user, channel, set, modes, args):
    nick = user.split("!")[0]
    if ("b" in modes) and (set==True):
        if nick in tbot.admins:
            tbot.say(channel, "You are the law.")
            return
        for index,b in enumerate(modes):
            tbot.logger.log("INFO", "Saw a ban by %s" % user)
            tbot.say(channel, "%s: %s Your ban will be removed in 30 seconds, to extend your ban, please ping a channel Admin." % (nick,choice(banresponses)))
            d = tbot.reactor.callLater(30, removeban, tbot, channel, args[index])
            tbot.mode(channel, False, "-o %s" % nick)
bandetect.modeChanged = True

def removeban(tbot, channel, ban):
    tbot.mode(channel, False, "-b %s" % ban)
