# Tried to implement, and thought it would be easier to have a server.py 
# Run the server, and then have clients connect to it (theoretically more than 2 players).
# The server would process and send other players data back to the clients, which would unpickle the information
# and update their respective gamespaces (each player would have their own game space).

# In this case, would need to "tick" on the server, then I got lost trying to figure out
# the LoopingCall

from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class GameConn(Protocol):
    def connectionMade(self):
        connections['game'] = self
    def dataReceived(self, data):
        # got players data


class GameFactory(Factory):
    game_protocol = GameConn

    # loop = LoopingCall(gs.iterate)
    # loop.start(float(1/60))

    def dataReceived(self, data):
        print data

class InitConn(Protocol):
    def connectionMade(self):
        connections['init'] = self
    game_server = TCP4ServerEndpoint(reactor, 9002)
    game_server.listen(GameFactory())
    self.transport.write("start game")

    def data_received(self, data):
        pass

class InitFactory(Factory):
    init_protocol = InitConn






if __name__ == '__main__':
    connections = {}
    game_data = {}
    
