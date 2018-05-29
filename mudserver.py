""" minorMud mudServer module
IMPORTANT: populate gamePlayers before running mudServer
Contains one class, mudServer which can be called to start a server
 which will handle all input/output to/from client/minorMud

author: Bob Hinkle - hinkle.bob@gmail.com
"""
import socket
import threading
import sys

HOST = '192.168.1.238'
PORT = 23456

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
# populate gamePlayers with [player.id,player.name,player.password]
gamePlayers = []  # to be populated with game.py TO VERIFY LOGIN!
players = []  # list of players connected
lock = threading.Lock()

# input from players will be placed on this stack to be processed
# format is [[player.id,<data>],]
inputStack = []

# output from game to players will be placed in this stack to be processed
# format is [[player.id, <message>],] or [['ALL', <message>],]
outputStack = []


class mudServer(threading.Thread):
    def __init__(self, sockAddress):
        threading.Thread.__init__(self)
        self.socket = sockAddress[0]
        self.address = sockAddress[1]

    def run(self):
        # Verify identity before appending players list
        self.name, self.id = self.logon()
        lock.acquire()
        players.append(self)
        lock.release()
        self.data = b''
        self.welcome()
        print('%s:%s connected.' % self.address)
        self.socket.setblocking(False)
        # loop!
        while True:
            # Process input from connection
            # Add input to inputStack to be processed by game.py
            viableInput = self.getInput()
            if(viableInput != -1):
                print("viableInput: ", viableInput)
                a = [self.id, viableInput]
                lock.acquire()
                inputStack.append(a)
                lock.release()
                self.data = b''
            # Process output from game.py
            # Check if stack contains either a message for player or ALL players
            lock.acquire()
            if(len(outputStack) > 0):
                for x in range(len(outputStack)):
                    print(outputStack, self.id)
                    if(outputStack[x][0] == self.id):
                        self.sendMessage(outputStack[x][1])
                        outputStack.pop(x)
                        break
                    # going to lock the thread before CHECKING for 'ALL'
                    # we don't want multiple threads grabbing this from the stack
                    #   at the same time
                    if(outputStack[x][0] == 'ALL'):
                        for p in players:
                            p.socket.send(outputStack[x][1].encode())
                        outputStack.pop(x)
                        break
            lock.release()
        self.logout()

    def logout(self):
        # Close player's connection gracefully
        self.socket.send(b'Goodbye...\r\n')
        self.socket.close()
        print('%s:%s disconnected.' % self.address)
        # if player was added to players list, remove them
        if(len(players) > 0):
            for player in players:
                if(player == self):
                    lock.acquire()
                    players.remove(self)
                    lock.release()
        sys.exit()

    def logon(self):
        # Verify LOGIN using gameplayers
        # Must return player.name, player.id
        flush = self.socket.recv(1024)  # this is used to clear bullshit upon connection
        flush = None
        player = self.username()
        if(player == -1):
            self.logout()
        else:
            verify = self.password(player)
            if(verify == -1):
                self.logout()
            else:
                return player[1], player[0]

    def welcome(self):
        self.socket.send(b"\x1b[31mWelcome ")
        self.socket.send(self.name.encode())
        self.socket.send(b", to minorMud!\r\n")
        for p in players:
            if(p.name != self.name):
                p.socket.send(self.name.encode())
                p.socket.send(b" has entered the game.\r\n")

    def sendMessage(self, text):
        self.socket.send(text.encode())

    def getInput(self):
        try:
            self.data += self.socket.recv(1024)
        except:
            pass
        # if a return/enter is detected, process input
        if(self.data.find(b'\r') != -1):
            return self.data.decode().split('\r\n')[0]
        else:
            return -1

    def getInputBlocking(self):
        data = b''
        while True:
            data += self.socket.recv(1024)
            if not data:
                self.logout()
            if(data.find(b'\r') != -1):
                return data.decode().split('\r\n')[0]

    def username(self):
        # Logon sequence to get username
        i = 0  # keep track of the login trys
        maxTrys = 3
        while i <= maxTrys:
            self.socket.send(b"Please enter your username (otherwise type 'new'): ")
            a = self.getInputBlocking()
            if(a.lower() == 'new'):
                self.newUser()
            else:
                for player in gamePlayers:
                    if(a.lower() == player[1].lower()):
                        return player
                self.socket.send(b"I'm sorry. Please try again...\r\n")
                i += 1
        self.socket.send(b'Too many tries...\r\n')
        return -1

    def password(self, player):
        i = 0
        maxTrys = 3
        while i <= maxTrys:
            self.socket.send(b"Password: ")
            a = self.getInputBlocking()
            if(a == player[2]):
                return 1
            else:
                self.socket.send(b"Incorrect. Try again.\r\n")
                i += 1
        return -1

    def newUser(self):
        # create later
        self.socket.send(b"Feature not yet implemented...")
        self.logout()


class acceptConnections(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            mudServer(s.accept()).start()
