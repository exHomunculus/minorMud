"""
This module will execute player commands; to be called by game.py
  This module will work in conjunction with game.py to help process
  commands from players. It must have access to the same objects as game.py

author: Bob Hinkle - hinkle.bob@gmail.com
"""
import ansi


class Command(object):
    """ This is the class for the command parser.
    Send user input here and recieve the appropriate actions in return
    All methods here will return a list of output strings to be sent to players
    the list will be formatted as [[player.id, text],]
    """

    def __init__(self, playerObject, mapObject):
        self.p = playerObject
        self.m = mapObject
        self.commands = ['give', 'equip', 'remove', 'go', 'sell',
                         'buy', 'look', 'inventory', 'spellbook', 'status',
                         'rest', 'sneak', 'attack', 'breakoff', 'who', 'top',
                         'steal', 'pick', 'bash', 'x', 'exit', 'party',
                         'health', 'n', 'ne', 'e', 'se', 's', 'sw', 'w',
                         'nw', 'u', 'd', '/', 'push', 'press', 'pull', 'experience']

    def parse(self, playerId, text, onlinePlayers):
        # check for trivial commands first
        if(text == ''):
            return self.refresh(playerId)
        elif(text == 'e'):
            return self.e(playerId)
        elif(text == 'w'):
            return self.w(playerId)
        elif(text == 'se'):
            return self.se(playerId)
        elif(text == 's'):
            return self.s(playerId)
        elif(text == 'n'):
            return self.n(playerId)
        self.onlinePlayers = onlinePlayers
        self.firstword = text.split(" ", 1)[0]
        if text.startswith('/'):
            return self.telepath(playerId, text)
        else:
            matching = []
            for command in self.commands:
                if command.startswith(self.firstword):
                    matching.append(command)
            # AUTOMATICALLY run associated method
            if len(matching) == 1:
                # splitting and saving everything after the matching command as subtext
                self.subtext = text.split(' ', 1)
                if(len(self.subtext) == 1):
                    # magic sauce - run a method by using text
                    return getattr(self, matching[0])(playerId, self.subtext)
                else:
                    return getattr(self, matching[0])(playerId, self.subtext[1])
            else:
                return self.say(playerId, text)

    def say(self, playerId, text):
        # just SAY something, will ya?
        # find other players in the same room with you
        output = []
        # this finds ALL players in the same room, even if offline
        players = self.p.getPlayersInSameRoom(playerId)
        realPlayers = []
        # we have to check against those players ACTUALLY online
        # we'll call them realPlayers
        for onlinePlayer in self.onlinePlayers:
            for allPlayer in players:
                if(onlinePlayer == allPlayer):
                    realPlayers.append(onlinePlayer)
        # now check for realPlayers/onlinePlayers in same room
        for player in realPlayers:
            if(int(player) == int(playerId)):
                # create a string for first person
                outString = ansi.COLOR['green'] + "You say, '" + text + "'\r\n" + ansi.COLOR['white']
                stackEntry = [player, outString]
                output.append(stackEntry)
            else:
                # create 3rd person string
                outString = ansi.COLOR['green'] + self.p.getName(playerId)[0] +\
                    " says, '" + text + "'\r\n" + ansi.COLOR['white']
                stackEntry = [player, outString]
                output.append(stackEntry)
        return output

    def refresh(self, playerId):
        # Basically, what happens when a player hits enter with nothing typed
        # right now, we're just displaying the current room
        # maybe redo this to use the MACROS
        for player in self.p.players:
            print("command, player[0]:", player[0], "playerId:", playerId)
            if(int(playerId) == int(player[0])):
                mapId = player[12]
        outString = self.m.briefView(mapId)
        stackEntry = [[playerId, outString], ]
        return stackEntry

    def give(self, subtext):
        helpm = "Typical useage:\r\nExample1: give <item> to <user>\r\nExample2: give <amount> <item> to <user>\r\n"
        contents = subtext.split(" ")
        if len(contents) == 4:
                # test if first item is an int
            if contents[0].isdecimal():
                # test is second item is object
                # test if third item is 'to'
                if contents[2] == 'to':
                    # test if fourth item is player
                    print("You give " + contents[0] + " " + contents[1] + " to Player " + contents[3])
                else:
                    print(helpm)
        elif len(contents) == 3:
            if contents[1] == 'to':
                print("You give " + contents[0] + " to player " + contents[2])
            else:
                print(helpm)
        else:
            print(helpm)

    def equip(self, subtext):
        help = "Typical useage:\r\nEquip <item>\r\n"
        # if item in player's inv
        # equip IF possible
        # may have to remove existing item before equipping
        # generate string(s) to display equip
        return help

    def remove(self, subtext):
        help = "Typical useage:\r\nRemove <item>\r\n"
        # if item equipped
        # remove
        # generate string(s) to display removal
        return help

    def go(self, subtext):
        help = "Typical useage:\r\nGo <place>\r\n"
        # if room has go-able place
        # move player to place
        # generate string(s) for movement
        # else generate string(s) for failure
        return help

    def sell(self, subtext):
        # if player's inv contains item
        # AND shop/room can sell/buy item
        # remove item from player's inv
        # calculate purchase cost and add to player's inv
        # generate string(s) for purchase
        # else generate string(s) for failure
        return 1

    def buy(self, subtext):
        # if shop/room has item
        # AND player's inv contains enough money
        # deduct money from player's inv
        # add item to player's inv
        # generate success OR failure string(s)
        return 1

    def look(self, subtext):
        # determine item or direction
        # if item, just pull description from item
        # if room, pull description from room
        # if used ALONE with no args, pull current room description
        # or generate failure string "you don't see golden chalice here!"
        return 1

    def inventory(self, subtext):
        # query player's inventory
        # create pretty string to display inventory
        return 1

    def spellbook(self, subtext):
        # if player has a spellbook
        # query it for learned spells
        # generate success OR failure string(s)
        return 1

    def status(self, subtext):
        # query stats on player
        # return pretty string to display player stats
        return 1

    def rest(self, subtext):
        # break combat IF in combat
        # enter accelerated HP regen mode
        # player object should have a method for calculating HP regen
        return 1

    def sneak(self, subtext):
        # if player capable of sneaking
        # enter sneaky movement mode
        # player object should have a method for determining sneaking success upon movement
        # generate success OR failure string(s)
        return 1

    def attack(self, subtext):
        # if target exists in current room
        # AND room is a combat area
        # begin attack mode
        return 1

    def breakoff(self, subtext):
        # if in attack/combat mode
        # breakoff combat
        # generate success OR failure string(s)
        return 1

    def who(self, subtext):
        # query mudServer for all connected players
        # create a pretty string to display players
        return 1

    def top(self, subtext):
        # if used alone
        # display top 10 players ever based on EXP
        # if used with subtext and that text is an int
        # display top X players
        return 1

    def steal(self, subtext):
        # if player has ability to steal
        # AND room is a combat area
        # query steal % from player object
        # if successful remove random FREE item from target
        # cannot steal an equipped item
        # money is stolen as a priority but not garaunteed
        # if failure, notify target and flag player as initiator of PVP
        return 1

    def pick(self, subtext):
        # if player has the ability to pick locks/traps
        # query success rate player vs object's picklocks
        # generate success OR failure string(s)
        # if door, unlock it
        # if treasurebox, unlock it
        # if trap, disarm it OR set it OFF
        return 1

    def bash(self, subtext):
        # if direction
        # AND door
        # query player object for chance vs door str
        # if monster
        # AND it's in present room
        # AND the room is a combat area
        # begin combat/attack mode using BASH modifier
        return 1

    def x(self, subtext=''):
        self.exit()

    def exit(self, subtext=''):
        # let the player EXIT the game gracefully
        return 1

    def party(self, subtext):
        # if player in party
        # create pretty string to display party stats
        return 1

    def health(self, subtext):
        # create a pretty string to display player health/mana
        return 1

    # Direction methods, they will just forward to movement method --------------------------
    def n(self, pid, subtext=''):
        return self.direction(pid, 'n')

    def ne(self, pid, subtext=''):
        return self.direction(pid, 'ne')

    def e(self, pid, subtext=''):
        return self.direction(pid, 'e')

    def se(self, pid, subtext=''):
        return self.direction(pid, 'se')

    def s(self, pid, subtext=''):
        return self.direction(pid, 's')

    def sw(self, pid, subtext=''):
        return self.direction(pid, 'sw')

    def w(self, pid, subtext=''):
        return self.direction(pid, 'w')

    def nw(self, pid, subtext=''):
        return self.direction(pid, 'nw')

    def u(self, pid, subtext=''):
        return self.direction(pid, 'u')

    def d(self, pid, subtext=''):
        return self.direction(pid, 'd')

    def direction(self, pid, direction):
        # get player's room
        roomId = self.p.getRoom(pid)
        room = self.m.getRoom(roomId)
        # what DIR
        if(direction == 'n'):
            try:
                goingTo = self.m.decodeDirBlob(room[2])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'ne'):
            try:
                goingTo = self.m.decodeDirBlob(room[3])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'e'):
            try:
                goingTo = self.m.decodeDirBlob(room[4])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'se'):
            try:
                goingTo = self.m.decodeDirBlob(room[5])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 's'):
            try:
                goingTo = self.m.decodeDirBlob(room[6])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'sw'):
            try:
                goingTo = self.m.decodeDirBlob(room[7])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'w'):
            try:
                goingTo = self.m.decodeDirBlob(room[8])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'nw'):
            try:
                goingTo = self.m.decodeDirBlob(room[9])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'u'):
            try:
                goingTo = self.m.decodeDirBlob(room[10])[1]
            except:
                return self.bump(pid, direction)
        elif(direction == 'd'):
            try:
                goingTo = self.m.decodeDirBlob(room[11])[1]
            except:
                return self.bump(pid, direction)
        if(goingTo > 0):
            self.p.setRoom(pid, goingTo)
            return self.refresh(pid)
        else:
            return -1

    def bump(self, pid, dir):
        print("player:", pid, "just tried to go", dir, "and failed.")
        return [[pid, ansi.COLOR['red'] + "There is no exit in that direction.\r\n"]]
    # End direction/movement methods ---------------------------------------------------------

    def telepath(self, subtext):
        # use or create a currently playing user list
        # <----------------------- This needs to ACTUALLY contain players
        currentPlayers = ["Gumby", "Venloch", "Beowulf", "Avatar"]
        # remove / from string
        a = subtext.strip('/')
        # break string up from FIRST instance of ' '
        target, message = a.split(" ", 1)
        # IF target matches any currently playing players
        # create telepath strings for player and target containing message
        matching = []
        for player in currentPlayers:
            player = player.lower()
            if player.startswith(target.lower()):
                matching.append(player)
        if len(matching) == 1:
            # Send telepath strings to player & target
            print("Sending a telepath to " + matching[0].capitalize() + " from Hink containing message: " + message)
        else:
            failure = "Sorry! You have to be more specific."
            # Send string for failure
            return failure
        return -1

    def push(self, subtext):
        # subtext should contain object name
        # if pushable initiate push
        # else create fail message
        return 1

    def press(self, subtext):
        # subtext should contain object name
        # if pressable initiate press
        # else create fail message
        return 1

    def pull(self, subtext):
        # subtext should contain object name
        # if pullable initiate pull
        # else create fail message
        return 1

    def experience(self, subtext=''):
        # return player experience
        return 1
