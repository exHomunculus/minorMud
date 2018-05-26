""" minorMud mudServer module
IMPORTANT: populate gamePlayers before running mudServer
Contains one class, mudServer which can be called to start a server
 which will handle all input/output to/from client/minorMud

author: Bob Hinkle - hinkle.bob@gmail.com
"""
import socket
import threading

HOST = '192.168.1.238'
PORT = 23456

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
# populate gamePlayers with [player.id,player.name]
gamePlayers = []  # to be populated with game.py TO VERIFY LOGIN!
players = []  # list of players connected
lock = threading.Lock()

COLOR = {'black': b'\x1b[30m', 'red': b'\x1b[31m', 'green': b'\x1b[32m',
         'yellow': b'\x1b[33m', 'blue': b'\x1b[34m', 'magenta': b'\x1b[35m',
         'cyan': b'\x1b[36m', 'white': b'\x1b[37m'}
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
        while True:
            self.data += self.socket.recv(1024)
            if not self.data:
                break
            if(self.data.find(b'\r') != -1):
                a = [self.id, self.data]
                lock.acquire()
                inputStack.append(a)
                lock.release()
                self.data = b''
            if(len(outputStack) > 0):
                for x in range(len(outputStack)):
                    if(outputStack[x][0] == self.id):
                        self.sendMessage(outputStack[x][1].encode())
                        lock.acquire()
                        outputStack.pop(x)
                        lock.release()
                    # going to lock the thread before CHECKING for 'ALL'
                    # we don't want multiple threads grabbing this from the stack
                    #   at the same time
                    lock.acquire()
                    if(outputStack[x][0] == 'ALL'):
                        for p in players:
                            p.socket.send(outputStack[x][1].encode())
                        outputStack.pop(x)
                    lock.release()
        self.socket.close()
        print('%s:%s disconnected.' % self.address)
        lock.acquire()
        players.remove(self)
        lock.release()

    def logon(self):
        # Verify LOGIN using gameplayers
        # Must return player.name, player.id
        flush = self.socket.recv(1024)  # this is used to clear bullshit upon connection
        flush = None
        i = 0  # keep track of the login trys
        maxTrys = 3
        while i <= maxTrys:
            self.socket.send(b"Please enter your username (otherwise type 'new'): ")
            data = b''
            while True:
                data += self.socket.recv(1024)
                if not data:
                    break
                # if a return/enter is detected, process input
                if(data.find(b'\r') != -1):
                    a = data.decode().split('\r')[0]
                    # if they incoming connection just hits enter basically
                    if(a == ''):
                        self.socket.send(b'Uh...? Try again?')
                        i += 1
                        break
                    else:
                        for player in gamePlayers:
                            if a == player[1]:
                                # this is the magic sauce.
                                return player[1], player[0]
                        self.socket.send(b"I'm sorry, I couldn't find that name.")
                        i += 1
                        break

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
