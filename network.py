from game import GameSpace
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import sys

from Utilities import ANGLE
from Utilities import COORD
from Utilities import FIRE
from Utilities import HEALTH
game = GameSpace()
GAME_PORT = 8002
INIT_PORT = 8000
HOST_NAME = ""
FPS = 60

def send_data(data):
    connections['game'].transport.write(data)

####### "HOST" BRANCH ####################
# For receiving initial connection
class GameHostConn(Protocol):
    def connectionMade(self):
        print "Created game connection"
        connections['game'] = self
        game.main("p1", send_data)
        loop = LoopingCall(game.iteration)
        loop.start(float(1/60))

    def dataReceived(self, data):
       game.get_remote(data)

class GameHostFactory(ClientFactory):
    protocol = GameHostConn

class InitConn(Protocol):
    def connectionMade(self):
        print "Other player joined..."
        connections['init'] = self
        self.transport.write("start game")
        # Using listenTCP instead of endpoints to make code more flexible
        reactor.listenTCP(GAME_PORT, GameHostFactory()) # Initial connection made to 
    def dataReceived(self, data):
        pass

class InitFactory(ClientFactory):
    protocol = InitConn

##################################

##### CLIENT BRANCH############
class InitClientConn(Protocol):
    def connectionMade(self):
        connections['init'] = self
    def dataReceived(self, data):
        if(data == "start game"):
            reactor.connectTCP(HOST_NAME, GAME_PORT, GameClientFactory())


class InitClientFactory(ClientFactory):
    protocol = InitClientConn
    def startedConnecting(self, connector):
        print "Began Initial Connection"

    def clientConnectionLost(self, connector, reason):
        print "ERROR: Lost initial connection\n", reason
    def clientConnectionFailed(self, connector, reason):
        print "ERROR: Could not establish initial connection\n", reason

class GameClientConn(Protocol):
    def connectionMade(self):
        print "connected to game host"
        connections['game'] = self        
        game.main("p2", send_data)
        loop = LoopingCall(game.iteration)
        loop.start(float(1/60))
    def dataReceived(self, data):
       game.get_remote(data)

class GameClientFactory(ClientFactory):
    protocol = GameClientConn
    def startedConnecting(self, connector):
        print "Began game connection with host"
    def clientConnectionLost(self, connector, reason):
        print "ERROR: Lost Connection\n", reason
    def clientConnectionFailed(self, connector, reason):
        print "ERROR: Connection Failed\n", reason

#######################################

if __name__ == '__main__':
    connections = {}
    game_data = {} # to be passed to game function as keyword arguments
    # Determine if host, otherwise connect
    if(sys.argv[1] == "host"):
        reactor.listenTCP(INIT_PORT, InitFactory())
    elif(sys.argv[1] == "join"):
        HOST_NAME = sys.argv[2]
        reactor.connectTCP(sys.argv[2], INIT_PORT, InitClientFactory())
        
    # Start loop at 60FPS
    # loop = LoopingCall(game.iteration)
    # loop.start(float(1/FPS))

    reactor.run()


