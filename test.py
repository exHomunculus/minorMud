import map
import player

m = map.Map()
p = player.Player()

NORTH = 2
NE = 3
EAST = 4
SE = 5
SOUTH = 6
SW = 7
WEST = 8
NW = 9
UP = 10
DOWN = 11

ROOM_BLOB = 1


for x in range(1, 14):
    print(m.verboseView(str(x)))

adjacentRoom = m.decodeDirBlob( m.getRoom(1)[11] )[1]

p.room = m.decodeDirBlob( m.getRoom(1)[11] )[1]


var = 1
while var == 1 :  # This constructs an infinite loop
    print("Current ROOM: ")
    print(p.room)
    print(m.getRoom(p.room))
    print(m.getExits(p.room))
    
    direction = input("Enter a direction  :")


    if direction == 'n' :
      p.room = m.decodeDirBlob( m.getRoom(p.room)[NORTH] )[ROOM_BLOB]

    elif direction == 'ne':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[NE] )[ROOM_BLOB]

    elif direction == 'e':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[EAST] )[ROOM_BLOB]
      
    elif direction == 'se':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[SE] )[ROOM_BLOB]

    elif direction == 's':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[SOUTH] )[ROOM_BLOB]
      
    elif direction == 'sw':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[SW] )[ROOM_BLOB]

    elif direction == 'w':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[WEST] )[ROOM_BLOB]
      
    elif direction == 'nw':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[NW] )[ROOM_BLOB]      

    elif direction == 'u':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[UP] )[ROOM_BLOB]

    elif direction == 'd':
      p.room = m.decodeDirBlob( m.getRoom(p.room)[DOWN] )[ROOM_BLOB]   

    else:
      print("must enter a valid direction")    



