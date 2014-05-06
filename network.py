<<<<<<< HEAD
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

COMMAND_PORT = 40051
DATA_PORT = 8555
CLIENT_PORT = 7888 #The port that you have to SSH into


class InitFactory(Factory):
    init_prot = Initconn

class Initconn(Protocol):
    def connectionMade(self):
        connections['init'] = self
    pygame.quit()
    loop.stop()
    # Use server endpoint; easier to use wrapper around listenTCP()
    server_endpoint = TCP4ServerEndpoint(reactor, 9095)
    server_endpoint.listen(GameFactory())
    self.transport.write("start game")

    def dataReceived(self, data):
        pass


=======
DIR = "direction" # 'left', 'right', 'up', 'down'?
COORD = "xy" #'x, y tuple'
ANGLE = "angle" # 'degrees from 0'
FIRE = "fired" # 'bool if fired projectile or not'
HEALTH = "health" # 'current health to check death'    
>>>>>>> ec7650afe1022d93e79b6e130ab8e029bdc4a286
