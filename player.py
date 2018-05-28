"""
This module will handle all player functions
There is 2 main connections to this module.
The first being game.py and the second being muddata.py
We will be importing muddata and instantiating all data from the dB
This module will be imported by game.py to control all player data

Player data is currently partitioned as follows:
fname,lname,password,race,class,exp,level,str,mnd,spr,agi,room,gpoints,hp,mp

author: Bob Hinkle - hinkle.bob@gmail.com
"""

import muddata

dbname = 'test'

# Declare STATIC variables
ID = 0
FNAME = 1
LNAME = 2
PW = 3
RACE = 4
CLASS = 5
EXP = 6
LEVEL = 7
STR = 8
MND = 9
SPR = 10
AGI = 11
ROOM = 12
GPOINTS = 13
HP = 14
MP = 15


class Player(object):
    # Main player object
    # To instantiate and hold all players data
    def __init__(self, db=dbname):
        # create a connection to muddata and pull all player data
        self.md = muddata.MudData(db)
        self.players = self.md.getPlayers()

    """

    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    G E T S //////////////////////////////////////////////////////////////////////////////////
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    """

    def getPlayersForLogin(self):
        # Create a list of [[player.id, player.fname, player.password],]
        # to be called by game.py to populate gamePlayers in mudserver.py
        gamePlayers = []
        for player in self.players:
            entry = [player[ID], player[FNAME], player[PW]]
            gamePlayers.append(entry)
        return gamePlayers

    def getPlayersInSameRoom(self, playerId):
        # return a list with playerIDs of other players in room with the player passed in arg
        # The other players MUST be in the game! if not, ignore
        # list will be formatted as [id,id,id,id,]
        # find roomID of initial player first
        roomID = 0  # I dunno about this
        playersInSameRoom = []
        for player in self.players:
            if(player[ID] == int(playerId)):
                roomID = player[ROOM]
        for player in self.players:
            if(player[ROOM] == roomID):
                playersInSameRoom.append(player[ID])
        return playersInSameRoom

    def getPlayer(self, id):
        # return specific player data
        if(int(id) > 0):
            return self.players[int(id) - 1]
        else:
            return -1

    def getRoom(self, id):
        # return specific player's current roomID
        if(int(id) > 0):
            return self.players[int(id) - 1][ROOM]

    def getName(self, id):
        # return specific player's first and last name
        if(int(id) > 0):
            return self.players[int(id) - 1][FNAME], self.players[int(id) - 1][LNAME]

    def getPassword(self, id):
        # return specific player's password
        # THIS WILL BE CHANGED TO A MORE SECURE METHOD
        if(int(id) > 0):
            return self.players[int(id) - 1][PW]

    def getRace(self, id):
        # return specific player's RaceID
        if(int(id) > 0):
            return self.players[int(id) - 1][RACE]

    def getClass(self, id):
        # return specific player's ClassID
        if(int(id) > 0):
            return self.players[int(id) - 1][CLASS]

    def getExp(self, id):
        # return specific player's experience points
        if(int(id) > 0):
            return self.players[int(id) - 1][EXP]

    def getLevel(self, id):
        # return specific player's current Level
        if(int(id) > 0):
            return self.players[int(id) - 1][LEVEL]

    def getStats(self, id):
        # return specific player's stats
        if(int(id) > 0):
            self.stats = [self.players[int(id) - 1][STR],
                          self.players[int(id) - 1][MND],
                          self.players[int(id) - 1][SPR],
                          self.players[int(id) - 1][AGI]]
            return self.stats

    def getGp(self, id):
        # return specific player's Good points
        if(int(id) > 0):
            return self.players[int(id) - 1][GPOINTS]

    def getHpMp(self, id):
        # return specific player's HP and MP
        if(int(id) > 0):
            return self.players[int(id) - 1][HP], self.players[int(id) - 1][MP]

    """

    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    S E T S //////////////////////////////////////////////////////////////////////////////////
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    """

    def setRoom(self, id, roomID):
        # set specific player's current roomID
        if(int(id) > 0):
            self.players[int(id) - 1][ROOM] = roomID

    def setName(self, id, fname, lname):
        # set specific player's first and last name
        if(int(id) > 0):
            self.players[int(id) - 1][FNAME] = fname
            self.players[int(id) - 1][LNAME] = lname

    def setPassword(self, id, pw):
        # set specific player's password
        # THIS WILL BE CHANGED TO A MORE SECURE METHOD
        if(int(id) > 0):
            self.players[int(id) - 1][PW] = pw

    def setRace(self, id, raceID):
        # set specific player's RaceID
        if(int(id) > 0):
            self.players[int(id) - 1][RACE] = raceID

    def setClass(self, id, classID):
        # set specific player's ClassID
        if(int(id) > 0):
            self.players[int(id) - 1][CLASS] = classID

    def setExp(self, id, exp):
        # set specific player's experience points
        if(int(id) > 0):
            self.players[int(id) - 1][EXP] = exp

    def setLevel(self, id, level):
        # set specific player's current Level
        if(int(id) > 0):
            self.players[int(id) - 1][LEVEL] = level

    def setStats(self, id, stats):
        # set specific player's stats
        # please send list as argument in the following format:
        # [<str>,<mnd>,<spr>,<agi>]
        if(int(id) > 0):
            self.players[int(id) - 1][STR] = stats[0]
            self.players[int(id) - 1][MND] = stats[1]
            self.players[int(id) - 1][SPR] = stats[2]
            self.players[int(id) - 1][AGI] = stats[3]

    def setGp(self, id, gp):
        # set specific player's Good points
        if(int(id) > 0):
            self.players[int(id) - 1][GPOINTS] = gp

    def setHpMp(self, id, hp, mp):
        # set specific player's HP and MP
        if(int(id) > 0):
            self.players[int(id) - 1][HP] = hp
            self.players[int(id) - 1][MP] = mp

    """

    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    PLAYER PROCEDURAL METHODS //////////////////////////////////////////////////////////////
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    """
    # I'm omitting the int casting to repeat myself less!!!!

    def addHp(self, id, hp):
        # add HP to player
        # you can also use this method to SUBTRACT hp by using a negative #
        self.players[id - 1][HP] += hp

    def addMp(self, id, mp):
        # add MP to player
        # you can also use this method to SUBTRACT mp by using a negative #
        self.players[id - 1][MP] += mp

    def addExp(self, id, exp):
        # add exp to player
        self.players[id - 1][EXP] += exp

    def hpRegen(self, id):
        # perform an hp regen 'click'
        # if we perform a click every 5 seconds.. it'll take 5 mins to go from 0 to full
        hp = self.players[id - 1][HP] / 60
        return hp

    def rollHP(self, id):
        # determine total HP
        # definitely subject to change!
        # totalHp = level*(str/5)+str
        totalHp = self.getLevel(id) * (self.getStats(id)[0] / 5) + self.getStats(id)[0]
        return totalHp
