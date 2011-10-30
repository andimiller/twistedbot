from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import task
from importer import Importer
from logger import Logger
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
    logger = Logger()

    def kickedFrom(self, channel, kicker, message):
        self.logger.log("WARN","Kicked from %s by %s with message %s" % (channel, kicker, message))

    def userJoined(self, user, channel):
        self.logger.log("INFO","%s joined %s" % (user, channel))

    def userKicked(self, kickee, channel, kicker, message):
        self.logger.log("WARN","%s got kicked from %s by %s with message %s" % (kickee, channel, kicker, message))
        for f in self.userKickedFunctions:
            f(self, kickee, channel, kicker, message)

    def signedOn(self):
        self.logger.log("GOOD","Signed on as %s." % (self.nickname))
        for channel in self.factory.channels:
            self.join(channel)
        
    def joined(self, channel):
        self.logger.log("GOOD","Joined %s." % (channel))
        for j in self.joinedFunctions:
            j(self, channel)

    def privmsg(self, user, channel, msg):
        user = user.split("!")[0]
        self.logger.log("OKAY","%s: <%s> %s" % (channel,user,msg))
        for r in self.functions.keys():
            if r.match(msg):
                self.logger.log("INFO","Launching: %s" % self.functions[r])
                self.functions[r](self, user, channel, msg)

    def timepassed(logger):
        logger.log("INFO", "one minute passed")
        pass

    l = task.LoopingCall(timepassed, logger)
    l.start(60) # call every sixty seconds

class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, settings):
        self.channels = settings["channels"]
        self.nickname = settings["nickname"]
        self.admins = settings["admins"]
        i = Importer()
        self.functions = i.functions
        self.joined = i.joined
        self.userKicked = i.userKicked

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason)


