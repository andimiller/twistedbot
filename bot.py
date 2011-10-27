from twisted.words.protocols import irc
from twisted.internet import protocol
import re

class Plugins(object):
    def hello(self, tbot, user, channel, msg):
        tbot.msg(channel,"Greetings %s from %s!" % (user, channel))
    hello.rule = re.compile("hello TwistedBot")

class TwistedBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)
    plugins = Plugins()

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname)

    def joined(self, channel):
        print "Joined %s." % (channel)
        self.msg(channel, "Greetings %s! I am a friendly new IRC bot written in Twisted!" % channel)
        self.msg(channel, "I am event driven! I'm fully threaded! I even have dynamic module loading! and I'm currently 43 lines of python!")

    def privmsg(self, user, channel, msg):
        print msg
        if self.plugins.hello.rule.match(msg):
            self.plugins.hello(self, user, channel, msg)

class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, channel, nickname='TwistedBot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason)

import sys
from twisted.internet import reactor

if __name__ == "__main__":
    reactor.connectTCP('irc.aberwiki.org', 6667, TwistedBotFactory("#lolhax"))
    reactor.run()
