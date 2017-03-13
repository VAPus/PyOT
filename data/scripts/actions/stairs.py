# XXX: Loop over items instead and generate these id lists based on attributes.

#stairs = 410, 429, 411, 432, 4834, 1385, 1396, 4837, 4836, 3687, 3219, 3138, 8281, 5260, 5259, 9573, 9574, 3688, 5258, 9846, 3220, 459, 423, 4835, 8282, 8283, 433

#ramps = 1390, 1388, 1394, 1392, 1398, 1404, 3685, 6915, 8378, 6911, 1400, 8374, 3681, 1402, 3683, 6913, 8376, 3679, 6909, 7542, 8372, 7925, 7924
#rampsDown = 8561, 6920, 6924, 8565, 6128, 479, 6921, 8563, 6917, 8559, 6127, 8566, 6923, 6919, 8562, 8377, 8560, 475, 8564, 6922, 480, 6918, 476, 429

laddersUp = 1386
#laddersDown = 369, 370, 408, 409, 427, 428, 924, 3135, 3136, 5545, 5763, 8170, 8276, 8277, 8279, 8280, 8284, 8285, 8286, 8595, 8596, 9606, 8281, 410
#trapsAndHoles = 462, 9625, 294, 383, 392, 469, 470, 482, 484, 485, 489, 7933, 7938, 8249, 8250, 8251, 8252, 8253, 8254, 8255, 8256, 8323, 8380, 8567, 8585, 8972, 3137, 5731, 6173, 6174,
sewers=435, 7750, 430

stairs = set()
ladders = set()

ramps = set()

for itemId in game.item.items:
    if 'floorchange' in game.item.items[itemId]:
        stairs.add(itemId)

# Stairs
@register("walkOn", stairs)
def floorchange(creature, thing, position, **k):
    # Check if we can do this
    if not config.monsterStairHops and not creature.isPlayer():
        return False

    # Note this is the correct direction
    if thing.floorchange == "north":
        creature.move(NORTH, level=-1, ignorestairhop=True)
        
    elif thing.floorchange == "south":
        creature.move(SOUTH, level=-1, ignorestairhop=True)
        
    elif thing.floorchange == "east":
        creature.move(EAST, level=-1, ignorestairhop=True)
        
    elif thing.floorchange == "west":
        creature.move(WEST, level=-1, ignorestairhop=True)
        
    elif thing.floorchange == "down":  
        # This is a reverse direction, get the tile under it, then all four sides checked depending on it
        destPos = position.copy()
        destPos.z += 1
        destThing = destPos.getTile().getThing(1)
        if not destThing or destThing.name == "ladder" or not destThing.floorchange:
            newPos = position.copy()
            newPos.z += 1
            try:
                creature.teleport(newPos)
            except:
                creature.notPossible()
            #creature.move(SOUTH, level=1)
            #creature.move(NORTH)
        # Note: It's the reverse direction
        elif destThing.floorchange == "north":
            creature.move(SOUTH, level=1, ignorestairhop=True)
        elif destThing.floorchange == "south":
            creature.move(NORTH, level=1, ignorestairhop=True)
        elif destThing.floorchange == "west":
            creature.move(EAST, level=1, ignorestairhop=True)
        elif destThing.floorchange == "east":
            creature.move(WEST, level=1, ignorestairhop=True)

    return True
    
@register('dropOnto', stairs)
def itemFloorChange(creature, thing, position, onPosition, onThing, **k):
    if not position: return # Place event.
    newPos = position.copy()
    if thing.floorchange == "north":
        newPos.y -= 1
        newPos.z -= 1
        
    elif thing.floorchange == "south":
        newPos.y += 1
        newPos.z -= 1
        
    elif thing.floorchange == "east":
        newPos.x += 1
        newPos.z -= 1
        
    elif thing.floorchange == "west":
        newPos.x -= 1
        newPos.z -= 1
        
    elif thing.floorchange == "down":  
        # This is a reverse direction, get the tile under it, then all four sides checked depending on it
        newPos.z += 1
        destThing = newPos.getTile().getThing(1)

        if not destThing:
            pass # Keep it.

        # Note: It's the reverse direction
        elif destThing.floorchange == "north":
            newPos.y += 1
            
        elif destThing.floorchange == "south":
            newPos.y -= 1
            
        elif destThing.floorchange == "west":
            newPos.x += 1
            
        elif destThing.floorchange == "east":
            newPos.y -= 1
    
    try:
        onThing.remove()
    except:
        pass # On dragging, this is ok to fail.
    onThing.place(newPos)        
    
    return False

# Ladders up

@register("use", laddersUp)
def floorup(creature, thing, position, **k):
    if creature.inRange(position, 1, 1, 0):
        direction = creature.directionToPosition(position, True)
        if direction != None:
            creature.move(direction)

        creature.move(SOUTH, level=-1)

        """newPos = position.copy()
        crePos = creature.position.copy()
        newPos.z -= 1
        newPos.y += 1
        try:
            creature.teleport(newPos)
        except:
            creature.notPossible()"""

            
# Ramps    
if not config.monsterStairHops:
    @register("walkOn", stairs|ramps)
    def verifyRampWalk(creature, **k):
        # Check if we can walk on ramps
        if not creature.isPlayer():
            return False
            
# Sewer Gates

@register("use", sewers)
def sewer(creature, thing, position, **k):
    if creature.inRange(position, 1, 1, 0):
        crePos = creature.position.copy()
        newPos = position.copy()
        newPos.z += 1
        try:
            creature.teleport(newPos)
        except:
            creature.notPossible()
        if newPos.x > crePos.x:
            creature.turn(1)
        elif newPos.x < crePos.x:
            creature.turn(3)
        elif newPos.x == crePos.x and newPos.y > crePos.y:
            creature.turn(2)
        elif newPos.x == crePos.x and newPos.y < crePos.y:
            creature.turn(0)
        ##dont turn if on the grate
