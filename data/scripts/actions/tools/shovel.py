OPENED_HOLE = {294, 383, 392, 469, 470, 482, 484, 485, 489, 7933, 7938, 8249, 8250, 8251, 8252, 8253, 8254, 8255, 8256, 8323, 8380, 8567, 8585, 8972}
CLOSED_HOLE = 468, 481, 483, 7932, 8579
shovels = 2554, 5710
 
TILE_SAND = {9059, 231}
ITEM_SCARAB_COIN = 2159
MUD_HOLE = 489
TUMB_ENTRANCE = '1345'
SCARAB_TILE = '101'
SCARAB_TILE_A = '103'
SCARAB_COIN_TILE = '102'
SCARAB_COIN_TILE_A = '104'
 
@register("useWith", shovels)
def useShovel(creature, thing, position, onThing, onPosition, **k):
    if onThing.itemId in CLOSED_HOLE:
        if onThing.itemId == 8579:
            onThing = onThing.transform(8585)
        else:
            onThing = onThing.transform(onThing.itemId + 1)
    elif onThing.itemId in TILE_SAND:
        if onThing.hasAction(TUMB_ENTRANCE):
            if random.randint(1, 5) == 1:
                onThing = onThing.transform(MUD_HOLE)
                
        elif onThing.hasAction(SCARAB_TILE):
            if random.randint(1, 20) == 1:
                getMonster("Scarab").spawn(onPosition)
                onThing.addAction(SCARAB_TILE_A)

        elif onThing.hasAction(SCARAB_TILE_A):
            if random.randint(1, 40) == 1:
                onThing.addAction(SCARAB_TILE)
     
        elif onThing.hasAction(SCARAB_COIN_TILE):
            if random.randint(1, 20) == 1:
                Item(ITEM_SCARAB_COIN, 1).place(onPosition)
                onThing.addAction(SCARAB_COIN_TILE_A)
     
        elif onThing.hasAction(SCARAB_COIN_TILE_A):
            if random.randint(1, 40) == 1:
                onThing.addAction(SCARAB_COIN_TILE)
    else:
        creature.notPossible()
        return False
    onThing.decay()
    return True