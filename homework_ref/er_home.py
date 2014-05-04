#Esteban Rojas
#CSE 30332
#Twisted Primer
#04/30/14

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.defer import DeferredQueue
from twisted.internet import reactor

COMMAND_PORT = 40051
DATA_PORT = 8555
CLIENT_PORT = 7888 #The port that you have to SSH into

connectionsDict = {}

class CommandConn(Protocol):
    def connectionMade(self):
        print "Command Connection Made"
        self.transport.write("begin data connect")
        reactor.listenTCP(DATA_PORT, DataConnFactory())

    def dataReceived (self, data):
        pass

    def connectionLost(self, reason):
        print "Command connection lost"


class CommandConnFactory(Factory):

    def buildProtocol(self, addr):
        protocol = CommandConn()
        connectionsDict["CommandConn"] = protocol
        return protocol;


class DataConn(Protocol):

    def __init__(self):

        self.queue = DeferredQueue()

    def connectionMade(self):
        print "connection made on DataConn"
        pass

    def dataReceived(self, data):
        self.queue.put(data)

    def sendData(self, data):
        connectionsDict["Client"].transport.write(data)
        self.queue.get().addCallback(self.sendData)

    def startForwarding(self):
        self.queue.get().addCallback(self.sendData)


class DataConnFactory(Factory):

    def buildProtocol(self, addr):
        protocol = DataConn()
        connectionsDict["DataConn"] = protocol
        return protocol


class ClientConn(Protocol):

    def __init__(self):

        self.queue = DeferredQueue()
        self.startForwarding()

    def connectionMade(self):
        print "connection made on ClientConn"
        
        #Start the chain of receiving data
        connectionsDict["DataConn"].startForwarding()

    def dataReceived(self, data):
        self.queue.put(data)

    def sendData(self, data):
        connectionsDict["DataConn"].transport.write(data)
        self.queue.get().addCallback(self.sendData)

    def startForwarding(self):
        self.queue.get().addCallback(self.sendData)


class ClientConnFactory(Factory):

    def buildProtocol(self, addr):
        protocol = ClientConn()
        connectionsDict["Client"] = protocol
        return protocol;



        


if __name__ == "__main__":
    reactor.listenTCP(COMMAND_PORT, CommandConnFactory())
    reactor.listenTCP(CLIENT_PORT, ClientConnFactory())
    reactor.run()

