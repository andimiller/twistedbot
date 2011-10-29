from twisted.words.protocols import irc
from twisted.internet import protocol
from datetime import datetime
from importer import Importer
import pygments.console
import re

class TwistedBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    def _get_functions(self):
        return self.factory.functions
    def _get_joined(self):
        return self.factory.joined
    def _get_userKicked(self):
        return self.factory.userKicked
    nickname = property(_get_nickname)
    functions = property(_get_functions)
    joinedFunctions = property(_get_joined)
    userKickedFunctions = property(_get_userKicked)

    versionName = "TwistedBot"
    versionNum = "v0.1"
    sourceURL = "https://bitbucket.org/Sylnai/twistedbot/"

    loglevels = {
            0: "green",
            1: "white",
            2: "yellow",
            3: "orange",
            4: "red"
            }

    def _logit(self, loglevel, message):
        m = "%s %s" % (datetime.now().strftime("%H:%M:%S"), message)
        print pygments.console.colorize(self.loglevels[loglevel], m)

    def kickedFrom(self, channel, kicker, message):
        self._logit(4,"Kicked from %s by %s with message %s" % (channel, kicker, message))

    def userJoined(self, user, channel):
        self._logit(2,"%s joined %s" % (user, channel))

    def userKicked(self, kickee, channel, kicker, message):
        self._logit(3,"%s got kicked from %s by %s with message %s" % (kickee, channel, kicker, message))
        for f in self.userKickedFunctions:
            f(self, kickee, channel, kicker, message)

    def signedOn(self):
        self.join(self.factory.channel)
        self._logit(0,"Signed on as %s." % (self.nickname))

    def joined(self, channel):
        self._logit(0,"Joined %s." % (channel))
        for j in self.joinedFunctions:
            j(self, channel)

    def privmsg(self, user, channel, msg):
        user= user.split("!")[0]
        self._logit(1,"%s: <%s> %s" % (channel,user,msg))
        for r in self.functions.keys():
            if r.match(msg):
                self._logit(0,"Launching: %s" % self.functions[r])
                self.functions[r](self, user, channel, msg)

class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, channel, nickname='TwistedBot'):
        self.channel = channel
        self.nickname = nickname
        i = Importer()
        self.functions = i.functions
        self.joined = i.joined
        self.userKicked = i.userKicked

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason)


