import socket
from server import Server

def main():
    """Main method for the server application, the server runs from here"""
    #Makes a new instance of the server class
    _server = Server()
    print("Starting up on %s port %s" % _server.server_add)
    #Binds the server to the given address
    _server.sck.bind(_server.server_add)
    #Listens for connections
    _server.sck.listen(1)
    print("Starting the game")
    #Runs the game logic
    _server.main_game()

if __name__ == '__main__':
    main()