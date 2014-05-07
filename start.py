# Attempt to build client interface here, which would launch the gamespace


from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory

SERVER = "student00.cse.nd.edu"

class InitClient(Protocol):
    def dataReceived(self, data):
        if(data == "start game"):
            reactor.connectTCP(SERVER, 9002, PlayerClientFactory)

class InitFactory(ClientFactory):
    def buildProtocol(self, addr):
        connections['init'] = Initclient()
    return connections['init']

class PlayerClient(Protocol):
    def dataReceived(self, data):
        # received other player's data

class PlayerClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print "Started to connect...\n"

    def buildProtocol(self, addr):
        connections['game'] = PlayerClient()
    loop = LoopingCall(game.iterate)
    loop.start(float(1/60))
    return connections['game']


