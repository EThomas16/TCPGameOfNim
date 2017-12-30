"""One player version of Game of Nim with AI"""

import socket
import sys
import time
from server import Server

class Client(Server):

    def __init__(self):
        super().__init__()

    def send(self, message):
        """Handles the sending of messages"""
        self.sck.sendto(message.encode(), self.server_add)

    def receive(self):
        """Handles the receiving of messages"""
        data = self.sck.recv(self.buffer)
        # The data needs to be decoded, otherwise it will use the bytes-like format it was sent in
        # It is also cast to a string to be used in the conditional statements
        data = str(data.decode())
        return data

    def set_current_turn(self, data):
        """Used in setting the current turn so that the client knows it is its move"""
        if "not" in data:
            # If the server says it's not the client's turn, sets current turn as false
            self.current_turn = False

        elif "yes" in data:
            #Gets the appropriate section of the sent data to set as the remaining value
            self.remain = int(data[3:])
            #This value is then displayed to the user to show how many marbles are remaining
            print("%d marbles remaining" % self.remain)
            # If the server says it is the client's turn, sets current turn to true
            self.current_turn = True

    def set_difficulty(self):
        """Allows the client to set the difficulty of the game"""
        # If the client goes first, it is allowed to set the difficulty
        difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
        # Converting to lower case is used for consistency in conditional statements
        difficulty = difficulty.lower()
        self.send(difficulty)

    def current_turn_logic(self):
        """Handles the displaying of the current turn to the client, as well as sending the client's choice
        to the server"""
        message = input("Please enter how many marbles you want to remove\n")
        #Sets the remaining marbles as the input subtracted from the current remaining value
        remaining = self.remain - int(message)
        #... and then displays it to the user
        print("You removed ", int(message), " marbles, there are now ", remaining, " remaining")
        # Sends how many marbles the client wants to remove to the server for it to calculate
        self.send(message)
        self.current_turn = False

    def game_over_logic(self):
        """Handles the game over state, allowing the client to say if they want to play again"""
        win = self.sck.recv(self.buffer)
        win = win.decode()
        #print(win)
        # Handles if the game is over
        game_over = input("Game over! Do you want to play again? Y/N\n")
        # .lower() used again for consistency
        game_over = str(game_over.lower())
        # If the user does not want to continue, the connection closes
        if game_over == "n":
            # If the user does not want to play again, closes the connection
            print("Thank you for playing! Closing the connection...")
            self.sck.close()
            exit()
        # If the user wants to continue, the game is reset in the server
        elif game_over == "y":
            # If the user does want to play again, gets the server to re-initialise the game
            print("Restarting game...")
            self.send(game_over)

    def logic(self):
        """Handles the logic for the client, including sending and receiving messages"""
        #Loops whilst the connection is active
        while True:
            try:
                #Uses the receiving method to acquire the current message from the server
                data = self.receive()
                #If the server tells the client to set the difficulty, the difficulty is set
                if data == "difficulty" or data == "redodiff":
                    self.set_difficulty()

                #Finds current turn
                if data == "not" or "yes":
                    # If the server says it's not the client's turn, sets current turn as false
                    self.set_current_turn(data)

                #Handles the game logic for if it is the client's turn
                if self.current_turn or data == "redo":
                    if data == "redo":
                        print("Please re-enter the value, the last one was invalid")
                    self.current_turn_logic()
                #If the server tells the client the game is over, the game over state is set
                if "over" in data:
                    if data.find("player 2"):
                        print("The winner is the AI!")

                    elif data.find("player 1"):
                        print("The winner is you!")
                    #Runs the logic to allow the user to restart the game or close the connection
                    self.game_over_logic()

                else:
                    #Waits for the server to make its turn rather than constantly checking
                    # Waits patiently for the server's turn
                    print("Waiting for the server to respond...")
                    #Sleep is used here to prevent the client being overloaded with data
                    time.sleep(1)

            except Exception as e:
                #If an error is thrown, closes the socket for safety
                self.sck.close()