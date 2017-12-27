import socket
import sys
from random import randint

def game_init_one_player():
    print("hello")

def game_init_two_player():
    turn = randint(0,1)
    print(turn)

    if turn == 0:
        #Server first turn
        firstTurn = True
        print("Server first!")

    elif turn == 1:
        #Client first turn
        firstTurn = False
        print("Client first!")

    difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
    difficulty = difficulty.lower()
    if difficulty == "hard":
        remain = 100
        print("Hard selected: %d remaining" % remain)

    elif difficulty == "easy":
        remain = 20
        print("Easy selected: %d remaining" % remain)

    return firstTurn, remain

def logic(input, remain):
    """This handles the logic for the program, this can be expanded to include AI"""
    remain -= int(input)
    print("%d marbles remaining..." % remain)
    return remain

def send(message, sck, client):
    msg = str(message)
    sck.sendto(msg.encode(), client)

#def get(message):


def main():
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_add = ('localhost', 10000)
    print(sys.stderr, "starting up on %s port %s" % server_add)
    sck.bind(server_add)

    #Might need to use this?
    #Sets connection as blocking - TCP
    sck.setblocking(1)
    #Listens for connections
    sck.listen(1)

    #Game loop
    while True: #Change to remain > 0
        print(sys.stderr, "waiting for a connection")
        con, client_add = sck.accept()
        print("connection from", client_add)

        firstTurn, remain = game_init_two_player()
        if firstTurn:
            print(">server first turn")
            message = input("It's your turn first! Please enter how many marbles you wish to remove:\n")
            remain -= int(message)
            message = "The server just removed %d marbles!" % remain
            #Fixes when server is first, since client never knew when it was its turn
            con.sendall(message.encode())
            print("%d marbles remaining..." % remain)
        elif not firstTurn:
            #send(firstTurn, sck, server_add)
            print(">client first turn")
            msg = "hello"
            con.sendall(msg.encode())
        try:
            #print("connection from", client_add)
            currentTurn = ~firstTurn

            while remain > 0:
                #Change this value to change no. of bytes received
                if currentTurn:
                    #Client turn
                    message = "yes"
                    con.sendall(message.encode())
                    print(">client current turn...")
                    data = con.recv(1)
                    print("received '%s'" % data)
                    if data:
                        print("sending data back to the client")
                        #Calculates the new remaining value
                        remain = logic(int(data), remain)
                        currentTurn = False
                        #con.sendall(data)
                    else:
                        print("no more data from", client_add)
                        break

                elif not currentTurn:
                    #Server turn
                    print(">server current turn...")
                    print("Sending current turn to client")
                    message = "not"
                    con.sendall(message.encode())
                    print("server's turn now")
                    message = input("It's your turn! Please enter the number of marbles you wish to remove:\n")
                    remain = logic(message, remain)
                    print("%d marbles remaining..." % remain)
                    con.sendall(str(remain).encode())
                    currentTurn = True

        finally:
            #Closes the connection to clean up
            con.close()

if __name__ == '__main__':
    main()