import socket
import sys
import time
from server import Server

class Client(Server):

    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_add = ('localhost', 10000)

    def send(self, message):
        """Handles the sending of messages"""
        self.sck.sendto(message.encode(), self.server_add)

    def logic(self):
        """Handles the logic for the client, including sending and receiving messages"""
        #Loops whilst the connection is active
        while True:
            try:
                """received = 0
                expected = len(message)
                while received < expected:"""
                currentTurn = False
                data = self.sck.recv(1024)
                #The data needs to be decoded, otherwise it will use the bytes-like format it was sent in
                #It is also cast to a string to be used in the conditional statements
                data = str(data.decode())
                #print("data is: ", data)
                #print("reached if statements")
                if data == "not":
                    #If the server says it's not the client's turn, sets current turn as false
                    currentTurn = False
                    #print("Server said no: ", currentTurn)

                elif data == "yes":
                    #If the server says it is the client's turn, sets current turn to true
                    currentTurn = True
                    #print("Server said yes: ", currentTurn)
                # received += len(currentTurn)

                elif data == "difficulty":
                    #If the client goes first, it is allowed to set the difficulty
                    difficulty = input("Please type which difficulty you want:\n>Hard\n>Easy\n")
                    #Converting to lower case is used for consistency in conditional statements
                    difficulty = difficulty.lower()
                    self.send(difficulty)


                elif data == "Do you want to play again? Y/N":
                    #Handles if the game is over
                    game_over = input("Game over! Do you want to play again? Y/N\n")
                    #.lower() used again for consistency
                    game_over = str(game_over.lower())
                    #If the user does not want to continue, the connection closes
                    if game_over == "n":
                        #If the user does not want to play again, closes the connection
                        print("Thank you for playing! Closing the connection...")
                        self.sck.close()
                        break
                    #If the user wants to continue, the game is reset in the server
                    elif game_over == "y":
                        #If the user does want to play again, gets the server to re-initialise the game
                        print("Restarting game...")
                        self.send(game_over)
                #Handles the game logic for if it is the client's turn
                if currentTurn or data == "redo":
                    if data == "redo":
                        print("Please re-enter the value, the last one was invalid")

                    #print("current turn is true, reached if statement")
                    #remain = self.sck.recv(1024)
                    print("Your turn... Standing by")
                    #print("There are %d marbles remaining" % remain)
                    message = input("Please enter how many marbles you want to remove\n")
                    print("sending '%s'" % message)
                    # sck.sendto(message.encode(), server_add)
                    #Sends how many marbles the client wants to remove to the server for it to calculate
                    self.send(message)
                    currentTurn = False
                    print("Current turn is now: ", currentTurn)
                    # print(sys.stderr, "received '%s'" % data)
                else:
                    #Waits for the server to make its turn rather than constantly checking
                    print("Waiting for server's turn... Waiting for 1 seconds...")
                    # Waits patiently for the server's turn
                    time.sleep(1)

                print("received %s" % data)

            except Exception as e:
                #If the game is over or something goes horribly wrong, closes the connection
                #If an error is thrown, closes the socket for safety
                self.sck.close()
                #print("Exception thrown in client.py: ", e)

            """finally:
                print(sys.stderr, "closing socket")
                sck.close()"""

