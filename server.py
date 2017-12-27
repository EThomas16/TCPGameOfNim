import socket
import sys
from random import randint

class Server():
    def __init__(self):
        #Sets the connection values
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_add = ('localhost', 10000)
        #Counts the number of remaining marbles
        self.remain = 0
        #Stores the currently connected clients
        self.clients = []

    def game_init_one_player(self):
        print("hello")

    def game_over(self, con):
        game_over = "Do you want to play again? Y/N"
        con.sendall(game_over.encode())
        # game_over = str(game_over.lower())
        data = con.recv(1024)
        data = str(data.lower())

        if data == "b'y'":
            print("Reinitialising the game")
            self.game_init_two_player()

        elif data == "b'n'":
            print("Game over, connection closing!\n")
            con.close()

    def game_init_two_player(self):
        """Initialises the game for two players, setting the difficulty and which player goes first"""
        #Generates a random number to decide which player, player 1 or player 2, goes first
        turn = randint(0,1)
        #If the number returned is zero, the server goes first
        if turn == 0:
            #Server first turn
            firstTurn = True
            print("Server first!")
        #If the number returned is one, the client goes first
        elif turn == 1:
            #Client first turn
            firstTurn = False
            print("Client first!")
        #Alter this to allow client to set difficulty
        difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
        difficulty = difficulty.lower()
        if difficulty == "hard":
            self.remain = randint(2,100)
            print("Hard selected: %d remaining" % self.remain)

        elif difficulty == "easy":
            self.remain = randint(2,20)
            print("Easy selected: %d remaining" % self.remain)

        return firstTurn

    def logic(self, input):
        """This handles the logic for the program, this can be expanded to include AI"""
        self.remain -= int(input)
        print("%d marbles remaining..." % self.remain)

    def send(self, message, client):
        msg = str(message)
        self.sck.sendto(msg.encode(), client)


    def game_two_players(self):
        """Main logic for the two player version of the game, takes the socket as a parameter to allow for message sending and receiving"""
        # Game loop
        while True:  # Change to remain > 0
            print(sys.stderr, "waiting for a connection")
            con, client_add = self.sck.accept()
            print("connection from", client_add)

            firstTurn = self.game_init_two_player()
            if firstTurn:
                print(">server first turn")
                message = input("It's your turn first! Please enter how many marbles you wish to remove:\n")
                self.remain -= int(message)
                message = "The server just removed %d marbles!" % self.remain
                # Fixes when server is first, since client never knew when it was its turn
                con.sendall(message.encode())
                print("%d marbles remaining..." % self.remain)
            elif not firstTurn:
                # send(firstTurn, sck, server_add)
                print(">client first turn")
                msg = "hello"
                con.sendall(msg.encode())
            try:
                # print("connection from", client_add)
                currentTurn = ~firstTurn

                while True:
                    # Change this value to change no. of bytes received
                    if self.remain > 0:
                        if currentTurn:
                            # Client turn
                            message = "yes"
                            con.sendall(message.encode())
                            print(">client current turn...")
                            data = con.recv(1)
                            print("received '%s'" % data)
                            if data:
                                print("sending data back to the client")
                                # Calculates the new remaining value
                                self.logic(int(data))
                                currentTurn = False
                                # con.sendall(data)
                            else:
                                print("no more data from", client_add)
                                break

                        elif not currentTurn:
                            # Server turn
                            print(">server current turn...")
                            print("Sending current turn to client")
                            message = "not"
                            con.sendall(message.encode())
                            print("server's turn now")
                            message = input("It's your turn! Please enter the number of marbles you wish to remove:\n")
                            self.logic(message)
                            print("%d marbles remaining..." % self.remain)
                            #con.sendall(str(self.remain).encode())
                            currentTurn = True

                    elif self.remain == 0:
                        self.game_over(con)
                        """print("Remain has reached %d" % remain)
                        game_over = "Do you want to play again? Y/N"
                        con.sendall(game_over.encode())
                        # game_over = str(game_over.lower())
                        data = con.recv(1024)
                        data = str(data.lower())

                        if data == "b'y'":
                            print("Reinitialising the game")
                            self.game_init_two_player()

                        elif data == "b'n'":
                            print("Game over, connection closing!\n")
                            con.close()"""

                    else:
                        self.game_over(con)

            except Exception as e:
                print("Exception thrown in two player connection: ", e)

            """finally:
                # Closes the connection to clean up
                con.close()"""