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
    def _get_main(self):
        return self.factory.main
    def _get_logger(self):
        return self.factory.logger
    nickname = property(_get_nickname)
    functions = property(_get_functions)
    joinedFunctions = property(_get_joined)
    userKickedFunctions = property(_get_userKicked)
    main = property(_get_main)
    logger = property(_get_logger)
    repos = [["Sylnai", "twistedbot", 35], ["Sylnai", "element80", 5]]

    versionName = "TwistedBot"
    versionNum = "v0.1"
    sourceURL = "https://bitbucket.org/Sylnai/twistedbot/"

    def init(self):
        self.logger.log("INFO", "Starting main loop")
        l = task.LoopingCall(self.mainloops,self.main)
        l.start(5, now=False)

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
            self.join(str(channel))
        
    def joined(self, channel):
        self.logger.log("GOOD","Joined %s." % (channel))
        for j in self.joinedFunctions:
            j(self, channel)

    def privmsg(self, user, channel, msg):
        user = user.split("!")[0]
        for r in self.functions.keys():
            if r.match(msg):
                self.functions[r](self, user, channel, msg)
                self.logger.log("INFO","Launched: %s" % self.functions[r])
        self.logger.log("OKAY","%s: <%s> %s" % (channel,user,msg))

    def say(self, channel, message, length = None):
        if isinstance(message, unicode):
            message=message.encode("utf-8")
        #hand off to normal msg function
        self.msg(channel, message, length)

    def mainloops(self, main):
        self.logger.log("INFO", "Doing main loops")
        if self.init > 0:
            for m in main:
                m(self)

class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, settings):
        for key in settings.keys():
            setattr(self, key, settings[key])
        self.logger = Logger(self.verbosity)
        self.logger.log("INFO", "Factory created")
        i = Importer(self.logger)
        self.functions = i.functions
        self.joined = i.joined
        self.userKicked = i.userKicked
        self.main = i.main

    def buildProtocol(self, addr):
        self.logger.log("INFO", "Building an instance of %s" % self.protocol)
        p = self.protocol()
        p.factory = self
        p.init()
        return p
    
    def startedConnecting(self, connector):
        self.logger.log("INFO", "Attempting to init new client")

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason)
