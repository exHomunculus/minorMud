"""
This module will run the game loop and handle game mechanics

We have a Command object to handle user input

author: Bob Hinkle - hinkle.bob@gmail.com
"""


class Command(object):
    """ This is the class for the command parser.
    Send user input here and recieve the appropriate actions in return
    """
    # Define commands!
    commands = ['give', 'equip', 'remove', 'go', 'sell',
                'buy', 'look', 'inventory', 'spellbook', 'status',
                'rest', 'sneak', 'attack', 'breakoff', 'who', 'top',
                'steal', 'pick', 'bash', 'x', 'exit', 'party',
                'health', 'n', 'ne', 'e', 'se', 's', 'sw', 'w',
                'nw', 'u', 'd', '/']
    # Associated help
    giveHelp = "Typical useage:\r\nExample1: give <item> to <user>\r\nExample2: give <amount> <item> to <user>\r\n"
    equipHelp = "Typical useage:\r\nEquip <item>\r\n"
    removeHelp = "Typical useage:\r\nRemove <item>\r\n"
    goHelp = "Typical useage:\r\nGo <place>\r\n"

    def __init__(self, text):
        global commands
        matching = []
        for command in commands:
            if command.startswith(text):
                matching.append(command)
        # we can add some code here to AUTOMATICALLY run associated method
        return matching

    def give(self, subtext):
        # if present in 1st player's inv
        # remove instance from 1st player's inv
        # add to 2nd player's inv
        # create string(s) to display transfer
        return 1

    def equip(self, subtext):
        # if item in player's inv
        # equip IF possible
        # may have to remove existing item before equipping
        # generate string(s) to display equip
        return 1

    def remove(self, subtext):
        # if item equipped
        # remove
        # generate string(s) to display removal
        return 1

    def go(self, subtext):
        # if room has go-able place
        # move player to place
        # generate string(s) for movement
        # else generate string(s) for failure
        return 1

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

    def party(self, subtext):
        # if player in party
        # create pretty string to display party stats
        return 1

    def health(self, subtext):
        # create a pretty string to display player health/mana
        return 1

    def movement(self, direction):
        # what DIR
        # utilize map object to determine if DIR is available
        # if it is, is there a door?
        # is it open? closed? locked/unlocked?
        # return string if closed
        # if open
        # use map object to find associated room#
        # move player
        return 1

    def telepath(self, subtext):
        # use or create a currently playing user list
        currentPlayers = []  # <----------------------- This needs to ACTUALLY contain players
        # remove / from string
        a = subtext.strip('/')
        # break string up from FIRST instance of ' '
        target, message = a.split(" ", 1)
        # IF target matches any currently playing players
        # create telepath strings for player and target containing message
        matching = []
        for player in currentPlayers:
            if player.startswith(target):
                matching.append(player)
        if len(matching) == 1:
                # Send telepath strings to player & target
            return 1
        else:
            failure = "Sorry! You have to be more specific."
            # Send string for failure
            return failure
        return 1
