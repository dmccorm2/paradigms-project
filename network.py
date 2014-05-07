# The idea here is to emulate what I saw in the other code,
# essentially a command line argument as to who is hosting and who is connecting

#<<<<<<< HEAD
DIR = 'direction' # 'left', 'right', 'up', 'down'?
COORD = 'xy' #'x, y tuple'
ANGLE = 'angle' # 'degrees from 0'
FIRE = 'fired' # 'bool if fired projectile or not'
HEALTH = 'health' # 'current health to check death'

from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import sys

INIT_PORT = 9001
GAME_PORT = 9002
START_GAME = "start game"
FPS = 60
HOST = "host"

####### "HOST" #######
# For receiving initial connection 


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

class GameHostFactory(Factory):
    protocol = GameHostConn

class GameHostConn(Protocol):
    def connectionMade(self):
        connections['hgame'] = self
    gs.main("p1")
    loop = LoopingCall(gs.iteration)
    loop.start(float(1/60))
     def dataReceived(self, data):
            game.get_remote(data)


class GameClientConn(Protocol):
    def dataReceived(self, data):
        gs.get_remote(data)

class GameClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        connections['game'] = self
    gs.main("p2")
    loop = LoopingCall(gs.iteration)
    loop.start(float(1/60)) 
    return connections['game']

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
        


    game = GameSpace()
    # Start loop at 60FPS
    loop = LoopingCall(game.iteration, game_data)
    loop.start(float(1/FPS))

    reactor.run()

#=======
DIR = "direction" # 'left', 'right', 'up', 'down'?
COORD = "xy" #'x, y tuple'
ANGLE = "angle" # 'degrees from 0'
FIRE = "fired" # 'bool if fired projectile or not'
HEALTH = "health" # 'current health to check death'    
#>>>>>>> ec7650afe1022d93e79b6e130ab8e029bdc4a286
