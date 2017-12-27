import socket
import sys
import time
from server import Server

class Client(Server):

    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_add = ('localhost', 10000)

    def send(self, message):
        self.sck.sendto(message.encode(), self.server_add)

    def logic(self):
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
                print("data is: ", data)
                #print("reached if statements")
                if data == "not":
                    currentTurn = False
                    print("Server said no: ", currentTurn)

                elif data == "yes":
                    currentTurn = True
                    print("Server said yes: ", currentTurn)
                # received += len(currentTurn)

                elif data == "Do you want to play again? Y/N":
                    game_over = input("Game over! Do you want to play again? Y/N\n")
                    game_over = str(game_over.lower())
                    if game_over == "n":
                        #If the user does not want to play again, closes the connection
                        print("Thank you for playing! Closing the connection...")
                        self.sck.close()
                        break

                    elif game_over == "y":
                        #If the user does want to play again, gets the server to re-initialise the game
                        print("Restarting game...")
                        self.send(game_over)

                if currentTurn:
                    print("current turn is true, reached if statement")
                    message = input("Please enter how many marbles you want to remove\n")
                    print("sending '%s'" % message)
                    # sck.sendto(message.encode(), server_add)
                    self.send(message)
                    currentTurn = False
                    print("Current turn is now: ", currentTurn)
                    # print(sys.stderr, "received '%s'" % data)
                else:
                    print("Waiting for server's turn... Waiting for 1 seconds...")
                    # Waits patiently for the server's turn
                    time.sleep(1)

                print("received %s" % data)

            except Exception as e:
                #If the game is over or something goes horribly wrong, closes the connection
                self.sck.close()
                #print("Exception thrown in client.py: ", e)

            """finally:
                print(sys.stderr, "closing socket")
                sck.close()"""

