import socket
from client import Client

def main():
    """Establishes the connection before calling the game logic from the client class"""
    _client = Client()
    print("connection %s port %s" % _client.server_add)
    #Connects to the server
    _client.sck.connect(_client.server_add)
    #Runs the logic for the client, which utilises information sent by the server
    _client.logic()

if __name__ == '__main__':
    main()