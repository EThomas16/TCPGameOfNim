import socket
import sys
import math
import time
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
        self.buffer = 1024
        self.num_check = False

    def game_init(self, con):
        """Initialises the game for two players, setting the difficulty and which player goes first"""
        #Generates a random number to decide which player, player 1 or player 2, goes first
        turn = randint(0,1)
        #If the number returned is zero, the server goes first
        if turn == 0:
            #Server first turn
            firstTurn = True
            difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
            difficulty = difficulty.lower()
            print("Server first!")
        #If the number returned is one, the client goes first
        elif turn == 1:
            #Client first turn
            firstTurn = False
            #Sends a message to the client, letting it know it can set the difficulty
            message = "difficulty"
            con.sendall(message.encode())
            #Receives and decodes the client's choice, which will then be used to set the difficulty
            difficulty = con.recv(self.buffer)
            difficulty = str(difficulty.decode())
            print("Client first!")

        if difficulty == "hard":
            #Generates a random value between 2 and 100 to set the initial marble stack as
            self.remain = randint(2,100)
            print("Hard selected: %d remaining" % self.remain)

        elif difficulty == "easy":
            #Generates a random value between 2 and 20 to set the initial marble stack as
            self.remain = randint(2,20)
            print("Easy selected: %d remaining" % self.remain)

        return firstTurn

    def logic(self, input):
        """This handles the logic for the program, this can be expanded to include AI"""
        #Decrements the current remaining marbles by the given amount
        print("Input: ", input, "\nRemaining: ", self.remain)
        if int((self.remain / 2)) >= int(input):
            self.remain -= int(input)
            print("%d marbles remaining..." % self.remain)
            print("Input: ", input, "\nNow Remaining: ", self.remain)
            self.num_check = False

        elif int(input) == 1 and int(self.remain) == 1:
            print("One remaining...")
            self.remain -= int(input)
            self.num_check = False

        else:
            #print("Invalid value received, please enter a value less than half of the remaining marbles")
            self.num_check = True

    def send(self, message, client):
        """Used to send messages (legacy?)"""
        msg = str(message)
        self.sck.sendto(msg.encode(), client)

    def receive(self, con):
        """Handles the receiving of data packets, checking the entire packet has been received"""
        print("end")

    def turn_order(self, con, currentTurn):
        while True:
            # Checks to see if there are marbles remaining
            if self.remain > 0:
                if currentTurn:
                    # Client turn
                    # Sends this message as a confirmation to the client that it is its turn
                    message = "yes"
                    con.sendall(message.encode())
                    print(">client current turn...")
                    #time.sleep(2)
                    #con.sendall(str(self.remain).encode())
                    # Receives any values the client entered and decodes it
                    data = con.recv(self.buffer)
                    data = data.decode()
                    print("received '%s'" % data)

                    if data:
                        print("sending data back to the client")
                        # Calculates the new remaining value
                        self.logic(int(data))
                        print(str(self.num_check))
                        currentTurn = False
                        if self.num_check:
                            #If the value is not valid, asks for another input from the client
                            message = "redo"
                            con.sendall(message.encode())
                            data = con.recv(self.buffer)
                            data = data.decode()
                            self.logic(int(data))
                            currentTurn = False

                        else:
                            currentTurn = False
                            message = "There are %d marbles left!" % self.remain
                            # Fixes when server is first, since client never knew when it was its turn
                            con.sendall(message.encode())
                            print("%d marbles remaining..." % self.remain)

                        # con.sendall(data)
                    else:
                        print("no more data from client")
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

                    if self.num_check:
                        message = input("Please re-enter a valid value:\n")
                        self.logic(message)
                        currentTurn = True

                    elif not self.num_check:
                        print("number valid?")
                        print("%d marbles remaining..." % self.remain)
                        currentTurn = True
                    # con.sendall(str(self.remain).encode())
            # If marbles has reached zero, runs the game over method
            elif self.remain == 0:
                self.game_over(con)
            # Else, sets game over anyway...
            else:
                self.game_over(con)

    def main_game(self):
        """Main logic for the two player version of the game, takes the socket as a parameter to allow for message sending and receiving"""
        # Game loop
        while True:
            #Waits for a client to connect before accepting a connection
            print(sys.stderr, "waiting for a connection")
            con, client_add = self.sck.accept()
            print("connection from", client_add)
            #Initialises the game once the client connects
            firstTurn = self.game_init(con)
            if firstTurn:
                #Server has first turn
                print(">server first turn")
                message = input("It's your turn first! Please enter how many marbles you wish to remove:\n")
                self.logic(message)

                if self.num_check:
                    message = input("Please re-enter a valid value:\n")
                    self.logic(message)

                elif not self.num_check:
                    message = "The server just removed %d marbles!" % self.remain
                    # Fixes when server is first, since client never knew when it was its turn
                    con.sendall(message.encode())
                    print("%d marbles remaining..." % self.remain)

            elif not firstTurn:
                #Client has first turn
                # send(firstTurn, sck, server_add)
                print(">client first turn")
                print("Waiting for 2 seconds to initialise client connection...")
                #Having this delay ensures that the separate messages for the client's turn status
                #and the no. of marbles remaining are kept apart to prevent the client stalling
                time.sleep(2)
                message = "Difficulty set. %d marbles remaining!" % self.remain
                # Fixes when server is first, since client never knew when it was its turn
                con.sendall(message.encode())
                print("%d marbles remaining..." % self.remain)


            try:
                # print("connection from", client_add)
                #Inverts the current value of the first turn to get the initial value for the second turn
                currentTurn = ~firstTurn
                self.turn_order(con, currentTurn)

            #Can be changed to handle specific exceptions
            except Exception as e:
                print("Exception thrown in two player connection: ", e)
                con.close()

    def game_over(self, con):
        """Handles the game over state, checking if the client wants to play again or not"""
        game_over = "Do you want to play again? Y/N"
        con.sendall(game_over.encode())
        # game_over = str(game_over.lower())
        #Receives the user's choice of game over state
        #The data is decoded to convert to a true string type
        data = con.recv(self.buffer)
        data = str(data.lower().decode())

        if data == "y":
            #Resets the game if specified by the user
            print("Reinitialising the game")
            self.game_init(con)

        elif data == "n":
            #Else, ends the connection with the client if they want to quit
            print("Game over, connection closing!\n")
            con.close()