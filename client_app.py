import socket
from client import Client

def main():
    """Establishes the connection before calling the game logic from the client class"""
    #sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _client = Client()
    #server_add = ('localhost', 10000)
    print("connection %s port %s" % _client.server_add)
    _client.sck.connect(_client.server_add)
    #firstTurn = _client.sck.recv(1024)
    #Runs the logic for the client, which utilises information sent by the server
    _client.logic()

if __name__ == '__main__':
    main()