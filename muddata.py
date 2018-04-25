"""
This module will connect to an SQLite database which holds all of the mud data.

Contains one call MudData which should be instantiated when a mudserver is loaded.

author: Bob Hinkle - hinkle.bob@gmail.com
author: Oktavious
"""


import sqlite3


class MudData(object):
    """
    This object will check to see if an existing db exists, if not it will initialize
    a new db to hold all data.
    It will contain all methods to set/get all mud attributes.
    This object is a basic model for all mud data. If you want to create/change/delete
    game content. It will be done through this class.
    Content includes: Classes/Races/Items/Maps/Spells/NPCs/MOBs/Quests/UserData/etc..
    """

    def __init__(self, dbname='test'):
        # FUTUREIDEA ~ add address,logincredentials here to connect to remote db,
        #              we are using SQLITE for this version however.
        self.dbname = dbname
        # ADD CHECK HERE (see if db exists or not) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.db = sqlite3.connect(self.dbname)
        self.cur = self.db.cursor()

    def createRoom(self, roomVals):
        # This function accepts a particular list of values to create a new room.
        # RoomID(int), Name(string), N,NE,E,SE,S,SW,W,NW,U,D(all int),underwater(int),
        # darkness(int), environmentalSpellID(int),description(string), area(int)
        self.cur.execute("INSERT INTO rooms (id,name,n,ne,e,se,s,sw,w,nw,u,d,\
        				underwater,darkness,spell,description,area)\
        				VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", roomVals)
        # ADD CHECK FOR SUCCESSFUL COMPLETION
        self.db.commit()

    def updateRoom(self, roomVals):
        # If you want to change a room's values, use this method.
        self.cur.execute("UPDATE rooms SET " +
                         "name = " + roomVals[1] +
                         ", n = " + roomVals[2] +
                         ", ne = " + roomVals[3] +
                         ", e = " + roomVals[4] +
                         ", se = " + roomVals[5] +
                         ", s = " + roomVals[6] +
                         ", sw = " + roomVals[7] +
                         ", w = " + roomVals[8] +
                         ", nw = " + roomVals[9] +
                         ", u = " + roomVals[10] +
                         ", d = " + roomVals[11] +
                         ", underwater = " + roomVals[12] +
                         ", darkness = " + roomVals[13] +
                         ", spell = " + roomVals[14] +
                         ", description = " + roomVals[15] +
                         ", area = " + roomVals[16] +
                         " WHERE id = " + roomVals[0] + ";")
        # ADD CHECK FOR SUCCESSFUL COMPLETION
        self.db.commit()

    def deleteRoom(self, id):
        # If you want to delete a room from the db, use this method.
        # We only need to pass the id of the room.
        self.cur.execute("DELETE FROM rooms WHERE id = " + id + ";")
        # ADD CHECK FOR SUCCESSFUL COMPLETION
        self.db.commit()

    def getRoom(self, id):
        # Retrieve the values for the room.
        self.cur.execute("SELECT * FROM rooms WHERE id = " + id + ";")
        return self.cur.fetchall()

    def getMap(self):
        # Return all rooms
        self.cur.execute("SELECT * FROM rooms;")
        return self.cur.fetchall()

    def createPlayer(self, pVals):
        # Creates a new player
        # format: id, fname, lname, password, race, class, exp, level,
        # str, mnd, spr, agi, room, gpoints, hp, mp
        self.cur.execute("INSERT INTO players (id, fname, lname, password, race,\
        				class, exp, level, str, mnd, spr, agi, room, gpoints, hp, mp)\
        				VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", pVals)
        self.db.commit()

    def updatePlayer(self, pVals):
        # Updates a player's information
        self.cur.execute("UPDATE players SET " +
                         "fname = " + pVals[1] +
                         ", lname = " + pVals[2] +
                         ", password = " + pVals[3] +
                         ", race = " + pVals[4] +
                         ", class = " + pVals[5] +
                         ", exp = " + pVals[6] +
                         ", level = " + pVals[7] +
                         ", str = " + pVals[8] +
                         ", mnd = " + pVals[9] +
                         ", spr = " + pVals[10] +
                         ", agi = " + pVals[11] +
                         ", room = " + pVals[12] +
                         ", gpoints = " + pVals[13] +
                         ", hp = " + pVals[14] +
                         ", mp = " + pVals[15] +
                         " WHERE id = " + pVals[0] + ";")
        self.db.commit()

    def deletePlayer(self, id):
        self.cur.execute("DELETE FROM players WHERE id = " + id + ";")
        self.db.commit()

    def getPlayer(self, id):
        self.cur.execute("SELECT * FROM players WHERE id = " + id + ";")
        return self.cur.fetchall()

    def getDoor(self, id):
        self.cur.execute("SELECT * FROM doors WHERE id = " + id + ";")
        return self.cur.fetchall()

    def getThing(self, thing, id):
        # So instead of repeating myself for each variant of this I make a utility knife
        self.cur.execute("SELECT * FROM " + thing + " WHERE id = " + id + ";")
        return self.cur.fetchall()
