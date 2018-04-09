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
        self.md = muddata.MudData(db)
        self.map = self.md.getMap()

    def getRoom(self, id):
        # Return room values from map
        if(int(id) > 0):
            return self.map[int(id) - 1]
        else:
            return -1

    def getExits(self, id):
        # Create and return a string of viable exits for the room.
        # You need to pass this function the room id.
        if(int(id) > 0):
            a = self.map[int(id) - 1][2:12]
            b = {"n": a[0], "ne": a[1], "e": a[2], "se": a[3], "s": a[4],
                 "sw": a[5], "w": a[6], "nw": a[7], "u": a[8], "d": a[9]}
        self.exitString = ""
        for exit in b:
            if b[exit]:
                self.exitString += exit + ", "
        if(self.exitString == ""):
            self.exitString = "None"
        return "Obvious exits: " + self.exitString.rstrip(", ") + "\r\n"

    def briefView(self, id):
        room = self.getRoom(id)
        return room[1] + "\r\n" + self.getExits(id)
