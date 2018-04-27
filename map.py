"""
This module will contain the Map class. It will house all Map related functions.
It will also connect to the MudData module for set/get Room data from the dB.
Contains call to Map which should be instantiated when the Mud is loaded.

author: Bob Hinkle - hinkle.bob@gmail.com
"""
import muddata

# Change this to whatever the current name of the dB is.
dbname = 'test'


class Map(object):
    """
    This object will be loaded into memory when a player connects.
    """

    def __init__(self, db=dbname):
        # Connect to dB, create a list of all rooms called map
        self.md = muddata.MudData(db)  # Create the muddata object
        self.map = self.md.getMap()    # Use the muddata object to pull ALL rooms into map variable

    def getRoom(self, id):
        # Return room values from map
        if(int(id) > 0):                # Make sure the value isnt 0 (or negative) roomID starts @ 1
            return self.map[int(id) - 1]  # since array values start with 0, we'll -1 from id(arg)
        else:
            return -1

    def getExits(self, id):
        # Create and return a string of viable exits for the room.
        # You need to pass this function the room id.
        if(int(id) > 0):
            # Grab only the direction BLOBs from the room
            a = self.map[int(id) - 1][2:12]
            # Create a dictionary for each dir BLOB
            # This dictionary matches the intended directions (strings) with their BLOBs
            b = {"n": a[0], "ne": a[1], "e": a[2], "se": a[3], "s": a[4],
                 "sw": a[5], "w": a[6], "nw": a[7], "u": a[8], "d": a[9]}
        # Create an empty string to be returned
        self.exitString = ""
        # Iterate through dictionary
        for exit in b:
            # If the BLOB isn't null, save the string associated with it, courtesy of the dictionary
            if b[exit]:
                self.exitString += exit + ", "  # adding a comma. There could be more than 1 exit
        # If there were no exits, we don't want a blank string. We want there to be 'None'
        if(self.exitString == ""):
            self.exitString = "None"
        # Create return string. We strip the trailing ", " if there is one.
        return "Obvious exits: " + self.exitString.rstrip(", ") + "\r\n"

    def briefView(self, id):
        # This is the clean way to see a room.
        # It's the same as verboseView minus the room description.
        room = self.getRoom(id)  # pull room data from THIS map object, not the DB.
        # return roomName, return, newline, and the exits (courtesy of getExits)
        return room[1] + "\r\n" + self.getExits(id)

    def verboseView(self, id):
        # This is the dirty way to see a room.
        # It's the same as briefView except has the roomDescription added
        room = self.getRoom(id)
        return room[15] + "\r\n" + room[1] + "\r\n" + self.getExits(id)

    def encodeDirBlob(self, doorID, roomID, doorState):
        # pass an int of doorID, roomID, and doorState converts each to hex and combines them
        # return the combo to be used for the direction BLOB of a room
        # Add a check to make sure the IDs are in range of real IDs <-----------------
        # if they're not INTs, make them INTs
        d = int(doorID)
        r = int(roomID)
        s = int(doorState)
        return f'{d:03X}'f'{r:04X}'f'{s:b}'

    def decodeDirBlob(self, dirBlob):
        # pass it a dirBlob and it returns doorID, roomID, open/close
        if(len(dirBlob) == 8):
            return int(dirBlob[:3], 16), int(dirBlob[3:7], 16), int(dirBlob[7])
        else:
            # Maybe throw error here. dirBlob should be 7 hex digits and a bool = 8
            return 0
