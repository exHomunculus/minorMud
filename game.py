"""
This module will run the game loop and handle game mechanics


author: Bob Hinkle - hinkle.bob@gmail.com
"""
import mudserver
import player
import command
import map


# instantiate game objects
p = player.Player()
m = map.Map()
c = command.Command(p, m)
# Populate mudserver.gamePlayers so we can login existing players
mudserver.gamePlayers = p.getPlayersForLogin()
onlinePlayers = []
# start the thread to accept incoming connections
# this thread will actually open new threads to handle each incoming connection
mudserver.acceptConnections().start()


def updateOnlinePlayers():
    global onlinePlayers
    onlinePlayers.clear()
    if(len(mudserver.players) > 0):
        for person in mudserver.players:
            onlinePlayers.append(person.id)


while True:
    # update the online players list
    updateOnlinePlayers()
    # check the inputStack and see if we need to process some player commands
    if(len(mudserver.inputStack) > 0):
        for x in range(len(mudserver.inputStack)):
            print("game loop, inputStack[x]:", mudserver.inputStack[x])
            # based on player input, we will receive back stuff to send to player(s)
            # that's what outputList will contain
            outputList = c.parse(mudserver.inputStack[x][0], mudserver.inputStack[x][1], onlinePlayers)
            if(outputList != -1):
                # add the output to the outputStack, to be processed by gameserver
                for output in outputList:
                    mudserver.outputStack.append(output)
                # remove from input stack because the input has been handled
            mudserver.inputStack.pop(x)
