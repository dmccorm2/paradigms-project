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


####### "HOST" #######
# For receiving initial connection
class GameHostConn(Protocol):
    def connectionMade(self):
        connections['hgame'] = self
    game.main("p1")
    loop = LoopingCall(game.iteration)
    loop.start(float(1/60))

    def dataReceived(self, data):
        game.get_remote(data)

class GameHostFactory(Factory):
    protocol = GameHostConn

class InitConn(Protocol):
    def connectionMade(self):
        connections['init'] = self
    # Using listenTCP instead of endpoints to make code more flexible
    game_server = reactor.listenTCP(GameHostFactory(), GAME_PORT) # Initial connection made to 
    self.transport.write("start game")

    def dataReceived(self, data):
        pass

class InitFactory(Factory):
    init_prot = Initconn


class GameClientConn(Protocol):
    def dataReceived(self, data):
        game.get_remote(data)

class GameClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        connections['game'] = self
        return connections['game']

    game.main("p2")
    loop = LoopingCall(game.iteration)
    loop.start(float(1/60)) 

    def clientConnectionLost(self, connector, reason):
        print "ERROR: Lost Connection\n", reason
    def clientConnectionFailed(self, connector, reason):
        print "ERROR: Connection Failed\n", reason



if __name__ == '__main__':
    connections = {}
    game_data = {} # to be passed to game function as keyword arguments
    # Determine if host, otherwise connect

    if(sys.argv[1] == HOST):
        reactor.listenTCP(INIT_PORT, InitFactory())
    elif(sys.argv[1] == JOIN):
        reactor.connectTCP(sys.argv[2], GAME_PORT, ClientFactory())
        
    # Start loop at 60FPS
    loop = LoopingCall(game.iteration, game_data)
    loop.start(float(1/FPS))

    reactor.run()


