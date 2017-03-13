ropeSpots = 384, 418, 8278, 8592
openedHoles = 294, 383, 392, 469, 470, 482, 484, 485, 489, 7933, 7938, 8249, 8250, 8251, 8252, 8253, 8254, 8255, 8256, 8323, 8380, 8567, 8585, 8972
openTraps = 462, 9625
ladders = 369, 370, 408, 409, 427, 428, 430, 924, 3135, 3136, 5545, 5763, 8170, 8276, 8277, 8279, 8280, 8281, 8284, 8285, 8286, 8595, 8596, 9606
ropes = 2120, 7731
 
@register("useWith", ropes)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if onPosition.x == 0xFFFF:
        if onThing.itemId and not onThing.containerSize:
            creature.notPossible()
        return
    newPos = onPosition.copy()
    crePos = creature.position.copy()
 
    if onThing.itemId in ropeSpots:
        newPos.y += 1
        newPos.z -= 1
        creature.teleport(newPos)
        if newPos.x > crePos.x:
            creature.turn(1)
        elif newPos.x < crePos.x:
            creature.turn(3)
        else:
            creature.turn(2)
 
    elif onThing.itemId in openedHoles or onThing.itemId in openTraps or onThing.itemId in ladders:
        Pos = onPosition.copy()
        Pos.z += 1
        newPos.y += 1
        Creature = getTile(Pos).topCreature()
        item = getTile(Pos).bottomItems()
 
        if item:
            ItemPos =  getTile(Pos).bottomItems()[0]
            try:
                ItemPos.move(newPos)
            except:
                pass
 
        elif getTile(Pos).hasCreatures() and not item:
            try:
                Creature.teleport(newPos)
            except:
                pass
        else:
            creature.notPossible()
    else:
        creature.notPossible()