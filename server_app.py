import socket
from server import Server

def main():
    """Main method for the server application, the server runs from here"""
    _server = Server()
    #sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_add = ('localhost', 10000)
    #print(sys.stderr, "starting up on %s port %s" % server_add)
    print("Starting up on %s port %s" % _server.server_add)
    _server.sck.bind(_server.server_add)

    #Might need to use this?
    #Sets connection as blocking - TCP
    print("Setting blocking")
    _server.sck.setblocking(1)
    #Listens for connections
    _server.sck.listen(1)
    print("Starting the game")
    _server.game_two_players()

if __name__ == '__main__':
    main()