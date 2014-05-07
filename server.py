# Tried to implement, and thought it would be easier to have a server.py 
# Run the server, and then have clients connect to it (theoretically more than 2 players).
# The server would process and send other players data back to the clients, which would unpickle the information
# and update their respective gamespaces (each player would have their own game space).

# In this case, would need to "tick" on the server, then I got lost trying to figure out
# the LoopingCall
#from main import GameSpace 
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint



if __name__ == '__main__':
    connections = {}
    game_data = {}
   # gs = GameSpace()
    
