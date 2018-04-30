import sqlite3
import muddata
import map

dbname = 'test'

class Player(object):

    
    room = 1
	

    def __init__(self, dbname='test'):
        # FUTUREIDEA ~ add address,logincredentials here to connect to remote db,
        #              we are using SQLITE for this version however.
        self.dbname = dbname
        # ADD CHECK HERE (see if db exists or not) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.db = sqlite3.connect(self.dbname)
        self.cur = self.db.cursor()
		
    def setRoom(self, setRoom):
        # Return room values from map
        self.room = setRoom

    def updateRoom(self, id, newRoom):
        # Updates a player's information
        self.cur.execute("UPDATE players SET " +

                         " room = " + newRoom +

                         " WHERE id = " + id + ";")
        self.db.commit()        

		
    def getRoom(self):
        
        # Retrieve the values for the room.
        
        return self.room