"""One player version of Game of Nim with AI"""

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
        self.optimal = 0
        #Stores the currently connected clients
        self.clients = []
        self.buffer = 1024
        self.num_check = False
        self.current_turn = False

    def game_init(self, con, client_add):
        """Initialises the game for two players, setting the difficulty and which player goes first"""
        #Generates a random number to decide which player, player 1 or player 2, goes first
        turn = randint(0,1)
        #If the number returned is zero, the server goes first
        if turn == 0:
            #Server first turn
            first_turn = True
            # Sends a message to the client, letting it know it can set the difficulty
            message = "difficulty"
            self.send(message, client_add, con)
            # con.sendall(message.encode())
            # Receives and decodes the client's choice, which will then be used to set the difficulty
            difficulty = self.receive(con)
            #difficulty = con.recv(self.buffer)
            difficulty = str(difficulty)
            print("Server first!")
        #If the number returned is one, the client goes first
        elif turn == 1:
            #Client first turn
            first_turn = False
            #Sends a message to the client, letting it know it can set the difficulty
            message = "difficulty"
            self.send(message, client_add, con)
            #con.sendall(message.encode())
            #Receives and decodes the client's choice, which will then be used to set the difficulty
            difficulty = self.receive(con)
            difficulty = str(difficulty)
            print("Client first!")

        if difficulty == "hard":
            #Generates a random value between 2 and 100 to set the initial marble stack as
            self.remain = randint(2,100)
            print("Hard selected: %d remaining" % self.remain)

        elif difficulty == "easy":
            #Generates a random value between 2 and 20 to set the initial marble stack as
            self.remain = randint(2,20)
            print("Easy selected: %d remaining" % self.remain)

        return first_turn

    def logic(self, input):
        """This handles the logic for the program, this can be expanded to include AI"""
        #Decrements the current remaining marbles by the given amount
        #print("Input: ", input, "\nRemaining: ", self.remain)
        if input == "" or not str(input).isdigit():
            self.num_check = True
            print("Invalid type entered")

        elif int((self.remain / 2)) >= int(input):
            self.remain -= int(input)
            #print("%d marbles remaining..." % self.remain)
            print("Input: ", input, "\nMarbles Remaining: ", self.remain)
            self.num_check = False

        elif int(input) == 1 and int(self.remain) == 1:
            print("One remaining...")
            self.remain -= int(input)
            self.num_check = False

        else:
            #print("Invalid value received, please enter a value less than half of the remaining marbles")
            self.num_check = True

    def ai_logic(self):
        """The logic for the AI of the game, calculates the best value to use to beat the user"""
        val_check = [3, 7, 15, 31, 63]
        for val in val_check:
            if self.remain > val:
                # Calculates using the power of two (minus one) rule
                optimal = self.remain - val
                if optimal <= int(self.remain / 2):
                    # And sets the remaining to be that value
                    #self.remain -= self.optimal
                    # The AI states its move
                    print("I make my move! I remove %d marbles" % optimal)
                    return optimal

                else:
                    print("Optimal value too large, recalculating...")
                    # Can change the way it handles this
                    optimal = randint(1, int((self.remain / 2) - 1))
                    # The AI states its move
                    print("I make my move! I remove %d marbles" % optimal)
                    return optimal

                # After finding the first 'optimal' value to subtract from in the list, the loop breaks to end calculation
                break

            elif 0 < self.remain <= 3:
                # Loses the game...
                print("I have lost")
                optimal = 1
                return optimal

            else:
                # Just a catch all
                print("Looking for optimal value...")
                continue

    def send(self, message, client, con):
        """Used to send messages (legacy?)"""
        msg = str(message)
        con.sendto(msg.encode(), client)

    def receive(self, con):
        """Handles the receiving of data packets, checking the entire packet has been received"""
        data = con.recv(self.buffer)
        data = data.decode()
        return data

    def empty_check(self, val):
        try:
            val = float(val)
        except ValueError:
            pass
        self.num_check = val

    def turn_order(self, con, client_add):
        while True:
            # Checks to see if there are marbles remaining
            if self.remain > 0:
                if self.current_turn:
                    # Client turn
                    # Sends this message as a confirmation to the client that it is its turn
                    message = "yes"
                    self.send(message, client_add, con)
                    print(">client current turn...")
                    #time.sleep(2)
                    #con.sendall(str(self.remain).encode())
                    # Receives any values the client entered and decodes it
                    data = self.receive(con)
                    #data = con.recv(self.buffer)
                    #data = data.decode()
                    print("received '%s'" % data)

                    if data:
                        #print("sending data back to the client")
                        # Calculates the new remaining value
                        self.logic(data)
                        print(str(self.num_check))
                        self.current_turn = False
                        while self.num_check:
                            #If the value is not valid, asks for another input from the client
                            message = "redo"
                            self.send(message, client_add, con)
                            #con.sendall(message.encode())
                            data = self.receive(con)
                            #data = con.recv(self.buffer)
                            #data = data.decode()
                            self.logic(data)
                            self.current_turn = False

                        if not self.num_check:
                            self.current_turn = False
                            if self.remain > 0:
                                message = "There are %d marbles left!" % self.remain
                                # Fixes when server is first, since client never knew when it was its turn
                                self.send(message, client_add, con)
                                #con.sendall(message.encode())
                            print("%d marbles remaining..." % self.remain)

                        # con.sendall(data)
                    else:
                        print("no more data from client")
                        break

                elif not self.current_turn:
                    # Server turn
                    print(">server current turn...")
                    #print("Sending current turn to client")
                    message = "not"
                    self.send(message, client_add, con)
                    #con.sendall(message.encode())
                    #print("server's turn now")
                    #message = input("It's your turn! Please enter the number of marbles you wish to remove:\n")
                    message = self.ai_logic()
                    self.logic(message)
                    if self.num_check:
                        message = input("Please re-enter a valid value:\n")
                        self.logic(message)
                        self.current_turn = True

                    elif not self.num_check:
                        #print("number valid?")
                        print("%d marbles remaining..." % self.remain)
                        self.current_turn = True
                    # con.sendall(str(self.remain).encode())
            # If marbles has reached zero, runs the game over method
            elif self.remain == 0:
                print("Game over, running game_over method")
                self.game_over(con, client_add)
            # Else, sets game over anyway...
            """else:
                self.game_over(con)"""

    def main_game(self):
        """Main logic for the two player version of the game, takes the socket as a parameter to allow for message sending and receiving"""
        # Game loop
        while True:
            #Waits for a client to connect before accepting a connection
            print(sys.stderr, "waiting for a connection")
            con, client_add = self.sck.accept()
            print("connection from", client_add)
            #Initialises the game once the client connects
            first_turn = self.game_init(con, client_add)
            if first_turn:
                #Server has first turn
                print(">server first turn")
                #message = input("It's your turn first! Please enter how many marbles you wish to remove:\n")
                message = self.ai_logic()
                self.logic(message)

                if self.num_check:
                    message = input("Please re-enter a valid value:\n")
                    self.logic(message)

                elif not self.num_check:
                    message = "The server just removed %d marbles!" % self.remain
                    # Fixes when server is first, since client never knew when it was its turn
                    self.send(message, client_add, con)
                    #con.sendall(message.encode())
                    print("%d marbles remaining..." % self.remain)

            elif not first_turn:
                #Client has first turn
                # send(firstTurn, sck, server_add)
                print(">client first turn...")
                print("Waiting for 2 seconds to initialise client connection...")
                #Having this delay ensures that the separate messages for the client's turn status
                #and the no. of marbles remaining are kept apart to prevent the client stalling
                time.sleep(2)
                message = "Difficulty set. %d marbles remaining!" % self.remain
                # Fixes when server is first, since client never knew when it was its turn
                self.send(message, client_add, con)
                #con.sendall(message.encode())
                print("%d marbles remaining..." % self.remain)

            try:
                # print("connection from", client_add)
                #Inverts the current value of the first turn to get the initial value for the second turn
                time.sleep(2)
                self.current_turn = ~first_turn
                self.turn_order(con, client_add)

            #Can be changed to handle specific exceptions
            except Exception as e:
                print("Exception thrown in two player connection: ", e)
                con.close()

    def game_over(self, con, client_add):
        """Handles the game over state, checking if the client wants to play again or not"""


        if not self.current_turn:
            print("You won!")
            game_over = "over player 1"
            self.send(game_over, client_add, con)
            #con.sendall(game_over.encode())

        else:
            print("Client won!")
            game_over = "over player 2"
            self.send(game_over, client_add, con)
            #con.sendall(game_over.encode())

        #Gives the client time to catch up so the message is received
        time.sleep(1)
        self.send(game_over, client_add, con)
        #con.sendall(game_over.encode())
        # game_over = str(game_over.lower())
        #Receives the user's choice of game over state
        #The data is decoded to convert to a true string type
        data = self.receive(con)
        #data = con.recv(self.buffer)
        #data = str(data.lower().decode())

        #time.sleep(2)

        """if self.current_turn:
            win = "Server wins!"
            print(win)
            con.sendall(win.encode())

        elif not self.current_turn:
            win = "Server wins!"
            print(win)
            con.sendall(win.encode())"""

        if data == "y":
            #Resets the game if specified by the user
            print("Reinitialising the game")
            self.game_init(con)

        elif data == "n":
            #Else, ends the connection with the client if they want to quit
            print("Game over, connection closing!\n")
            con.close()