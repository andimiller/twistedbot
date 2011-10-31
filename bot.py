from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import task
from importer import Importer
from logger import Logger
from config import Config
import re

class TwistedBot(irc.IRCClient):
    versionName = "TwistedBot"
    versionNum = "v0.2"
    sourceURL = "https://bitbucket.org/Sylnai/twistedbot/"

    def init(self):
        self.logger.log("INFO", "Starting main loop")
        if getattr(self, "main"):
            l = task.LoopingCall(self.mainloops)
            l.start(30, now=False)

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
        for channel in self.channels:
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

    def mainloops(self):
        self.logger.log("INFO", "Doing main loop")
        for m in self.main:
            m(self)

class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, settings, config):
        self.config = Config(config)
        self.settings = settings
        self.logger = Logger(settings["verbosity"])
        self.logger.log("INFO", "Factory created")

    def buildProtocol(self, addr):
        self.logger.log("INFO", "Building an instance of %s" % self.protocol)
        p = self.protocol()
        p.factory = self
        p.logger = self.logger
        p.config = self.config
        #Migrate settings
        for key in self.settings.keys():
            setattr(p, key, self.settings[key])
        p.config = self.config
        #Migrate functions
        i = Importer(self.logger)
        p.functions = i.functions
        p.joinedFunctions = i.joined
        p.userKicked = i.userKicked
        p.main = i.main
        p.init()
        self.logger.log("WARN", "Main is: %s" % i.main)
        return p
    
    def startedConnecting(self, connector):
        self.logger.log("INFO", "Attempting to init new client")

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason)
