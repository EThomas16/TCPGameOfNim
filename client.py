import socket
import sys
import time

def send(message, sck, server):
    sck.sendto(message.encode(), server)

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_add = ('localhost', 10000)
print("connection %s port %s" % server_add)
sck.connect(server_add)
firstTurn = sck.recv(1024)

if not firstTurn:
    message = input("It's your turn first! Please enter how many marbles you wish to remove:\n")
    send(message, sck, server_add)
    currentTurn = False

while True:
    try:
        """received = 0
        expected = len(message)
        while received < expected:"""
        currentTurn = False
        data = sck.recv(1024)
        data = str(data)
        print("data is: ", data)
        print("reached if statements")
        if data == "b'not'":
            currentTurn = False
            print("Server said no: ", currentTurn)

        elif data == "b'yes'":
            currentTurn = True
            print("Server said yes: ", currentTurn)
        #received += len(currentTurn)
        if currentTurn:
            print("current turn is true, reached if statement")
            message = input("Please enter how many marbles you want to remove\n")
            print("sending '%s'" % message)
            # sck.sendto(message.encode(), server_add)
            send(message, sck, server_add)
            currentTurn = False
            print("Current turn is now: ", currentTurn)
            #print(sys.stderr, "received '%s'" % data)
        else:
            print("Waiting for server's turn... Waiting for 1 second...")
            time.sleep(1)

        print("received %s" % data)

    except Exception as e:
        print("hello", e)

    """finally:
        print(sys.stderr, "closing socket")
        sck.close()"""