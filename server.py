"""Two player version of Game of Nim without AI"""

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
        #Sets the buffer value for receiving data
        self.buffer = 1024
        #Initialises conditional variables used to check the status of the clients and inputs
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
            # Allows the user to set the difficulty
            difficulty = input("Invalid entry. Please type which difficulty you want:\n>Hard\n>Easy\n")
            while difficulty != "hard" and difficulty != "easy":
                difficulty = input("Please re-type which difficulty you want:\n>Hard\n>Easy\n")
                str(difficulty.lower())
                print(difficulty)
            print("Server first!")
        #If the number returned is one, the client goes first
        elif turn == 1:
            #Client first turn
            first_turn = False
            #Sends a message to the client, letting it know it can set the difficulty
            message = "difficulty"
            self.send(message, client_add, con)
            #Receives and decodes the client's choice, which will then be used to set the difficulty
            difficulty = self.receive(con)
            difficulty = str(difficulty.lower())
            while difficulty != "hard" and difficulty != "easy":
                # If the value is not valid, asks for another input from the client
                message = "redodiff"
                self.send(message, client_add, con)
                # Receives the new value
                difficulty = self.receive(con)
                difficulty = str(difficulty.lower())
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
        """This handles the logic for the program"""
        #Checks if the input is valid, if not num_check is set to true to tell the program to ask the user for another input
        #.isdigit() checks if the input contains numerical digits. If it does not, false is returned
        if input == "" or not str(input).isdigit():
            self.num_check = True
            print("Invalid type entered")
        #Checks if the input is less than half of the remaining to ensure the move is valid
        elif int((self.remain / 2)) >= int(input):
            #If the entry is valid, it is subtracted from the remaining marbles
            self.remain -= int(input)
            print("Input: ", input, "\nMarbles Remaining: ", self.remain)
            self.num_check = False

        elif int(input) == 1 and int(self.remain) == 1:
            #This prevents an issue where 1 could not be entered if only 1 marble remained
            print("One remaining...")
            self.remain -= int(input)
            self.num_check = False

        else:
            #Catches any other instances where there might not be a valid input
            self.num_check = True

    def send(self, message, client, con):
        """Used to send messages"""
        msg = str(message)
        con.sendto(msg.encode(), client)

    def receive(self, con):
        """Handles the receiving of data packets, checking the entire packet has been received"""
        data = con.recv(self.buffer)
        data = data.decode()
        return data

    def turn_order(self, con, client_add):
        """Handles the turn order for the game"""
        while True:
            # Checks to see if there are marbles remaining
            if self.remain > 0:
                if self.current_turn:
                    # Client turn
                    # Sends this message as a confirmation to the client that it is its turn
                    message = "yes%d" % self.remain
                    self.send(message, client_add, con)
                    time.sleep(1)
                    print(">client current turn...")
                    # Receives any values the client entered and decodes it
                    data = self.receive(con)
                    print("received '%s'" % data)
                    #If data received...
                    if data:
                        # Calculates the new remaining value
                        self.logic(data)
                        self.current_turn = False
                        #Loops until the user enters a valid value
                        while self.num_check:
                            #If the value is not valid, asks for another input from the client
                            message = "redo"
                            self.send(message, client_add, con)
                            #Receives the new value
                            data = self.receive(con)
                            #Runs the logic on the new value
                            self.logic(data)
                            self.current_turn = False

                        if not self.num_check:
                            #Else if valid the client's turn is ended
                            self.current_turn = False
                            print("%d marbles remaining..." % self.remain)

                    else:
                        #Just prints in the event the client sends no more data at all
                        print("no more data from client")
                        break

                elif not self.current_turn:
                    # Server turn
                    print(">server current turn...")
                    message = "not"
                    #Sends the message to the client to ensure it cannot make a move
                    self.send(message, client_add, con)
                    #Waits for the client to register the message being sent
                    time.sleep(1)
                    #Waits for an input
                    message = input("Please enter the number of marbles you want to remove:\n")
                    #Runs the logic method using the input from the user
                    self.logic(message)

                    while self.num_check:
                        message = input("Please re-enter a valid value:\n")
                        self.logic(message)
                        self.current_turn = True

                    if not self.num_check:
                        #Displays the remaining number of marbles and sets the server's turn as being over
                        print("%d marbles remaining..." % self.remain)
                        self.current_turn = True
            # If marbles has reached zero, runs the game over method
            elif self.remain == 0:
                print("Game over, running game_over method")
                #Runs the game over method to allow the client to restart the game or end the connection
                self.game_over(con, client_add)

    def main_game(self):
        """Main logic for the game, takes the socket as a parameter to allow for message sending and receiving"""
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
                #Asks for the user to enter a value since it is its turn first
                message = input("It's your turn first, please enter how many marbles you want to remove:\n")
                #... and then runs the logic method using this value
                self.logic(message)

                if self.num_check:
                    message = input("Please re-enter a valid value:\n")
                    self.logic(message)

                elif not self.num_check:
                    message = "%d marbles remaining" % self.remain
                    # Fixes when server is first, since client never knew when it was its turn
                    self.send(message, client_add, con)
                    print("%d marbles remaining..." % self.remain)

            elif not first_turn:
                #Client has first turn
                print(">client first turn...")
                print("Waiting for 2 seconds to initialise client connection...")
                #Having this delay ensures that the separate messages for the client's turn status
                #and the no. of marbles remaining are kept apart to prevent the client stalling
                time.sleep(2)
                message = "Difficulty set. %d marbles remaining!" % self.remain
                # Fixes when server is first, since client never knew when it was its turn
                self.send(message, client_add, con)
                print("%d marbles remaining..." % self.remain)

            try:
                time.sleep(2)
                #Inverts the current value of the first turn to get the initial value for the second turn
                self.current_turn = ~first_turn
                #Runs the turn_order method to calculate the main logic for the game
                self.turn_order(con, client_add)

            #Handles if there are any exceptions running the main method, printing the error as required
            except Exception as e:
                print("Exception thrown in two player connection: ", e)
                #Closes the connection to prevent occupying of a port
                con.close()

    def game_over(self, con, client_add):
        """Handles the game over state, checking if the client wants to play again or not"""
        if not self.current_turn:
            #If it wasn't the server's turn when the game ended, it wins
            print("You won!")
            game_over = "over player 1"
            #Tells the client the server won
            self.send(game_over, client_add, con)

        else:
            print("Client won!")
            game_over = "over player 2"
            #Tells the client it won
            self.send(game_over, client_add, con)

        #Gives the client time to catch up so the message is received
        time.sleep(1)
        self.send(game_over, client_add, con)
        #Receives the user's choice of game over state
        #The data is decoded to convert to a true string type
        data = self.receive(con)

        if data == "y":
            #Resets the game if specified by the user
            print("Reinitialising the game")
            self.game_init(con, client_add)

        elif data == "n":
            #Else, ends the connection with the client if they want to quit
            print("Game over, connection closing!\n")
            con.close()