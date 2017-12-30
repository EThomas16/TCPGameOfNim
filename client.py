"""One player version of Game of Nim with AI"""

import socket
import sys
import time
from server import Server

class Client(Server):

    def __init__(self):
        super().__init__()
        self.clock = 0
        #self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_add = ('localhost', 10000)

    def send(self, message):
        """Handles the sending of messages"""
        self.sck.sendto(message.encode(), self.server_add)

    def set_current_turn(self, data):
        if data == "not" or data[3:6] == "not":
            # If the server says it's not the client's turn, sets current turn as false
            print("Not")
            self.current_turn = False


        elif data == "yes" or data[3:6] == "yes":
            # If the server says it is the client's turn, sets current turn to true
            print("Yes")
            self.current_turn = True

    def set_difficulty(self):
        # If the client goes first, it is allowed to set the difficulty
        difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
        # Converting to lower case is used for consistency in conditional statements
        difficulty = difficulty.lower()
        self.send(difficulty)

    def current_turn_logic(self):
        print("Your turn... Standing by")
        # print("There are %d marbles remaining" % remain)
        message = input("Please enter how many marbles you want to remove\n")
        print("sending '%s'" % message)
        # sck.sendto(message.encode(), server_add)
        # Sends how many marbles the client wants to remove to the server for it to calculate
        self.send(message)
        self.current_turn = False
        print("Current turn is now: ", self.current_turn)
        # print(sys.stderr, "received '%s'" % data)

    def game_over_logic(self):
        win = self.sck.recv(self.buffer)
        win = win.decode()
        print(win)
        # Handles if the game is over
        game_over = input("Game over! Do you want to play again? Y/N\n")
        # .lower() used again for consistency
        game_over = str(game_over.lower())
        # If the user does not want to continue, the connection closes
        if game_over == "n":
            # If the user does not want to play again, closes the connection
            print("Thank you for playing! Closing the connection...")
            self.sck.close()
            return game_over
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
                #self.current_turn = False
                data = self.sck.recv(self.buffer)
                #The data needs to be decoded, otherwise it will use the bytes-like format it was sent in
                #It is also cast to a string to be used in the conditional statements
                data = str(data.decode())
                print("Current data:", data)

                if data == "difficulty":
                    print("Setting difficulty...")
                    self.set_difficulty()

                #Finds current turn
                if data == "not" or "yes":
                    # If the server says it's not the client's turn, sets current turn as false
                    self.set_current_turn(data)
                    print(self.current_turn)

                #Handles the game logic for if it is the client's turn
                if self.current_turn or data == "redo":
                    print("Running current turn logic")
                    if data == "redo":
                        print("Please re-enter the value, the last one was invalid")

                    self.current_turn_logic()

                elif "over" in data:
                    if data.find("player 1"):
                        print("The winner is: player 1!")

                    elif data.find("player 2"):
                        print("The winner is: player 2!")

                    self.game_over_logic()

                else:
                    #Waits for the server to make its turn rather than constantly checking
                    print("Waiting for server's turn... Waiting for 1 seconds...")
                    # Waits patiently for the server's turn
                    time.sleep(1)
                    self.clock += 1
                    if self.clock == 10:
                        print("Disconnected, closing connection...")
                        self.sck.close()

                print("received %s" % data)

            except Exception as e:
                #If the game is over or something goes horribly wrong, closes the connection
                #If an error is thrown, closes the socket for safety
                self.sck.close()
                #print("Exception thrown in client.py: ", e)

            """finally:
                print(sys.stderr, "closing socket")
                sck.close()"""

