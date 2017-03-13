ITEM_WHEAT = 2694
ITEM_FLOUR = 2692
ITEM_DOUGH = 2693
ITEM_BREAD = 2689
ITEM_MILL = (1381, 1382, 1383, 1384)
TYPE_EMPTY = 0
TYPE_WATER = 1
OVEN_ON = (1786, 1788, 1790, 1792, 6356, 6358, 6360, 6362)

@register("useWith", (2692, 2693, 2694))
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if thing.itemId == ITEM_WHEAT and onThing.itemId in ITEM_MILL:
        creature.addItem(Item(ITEM_FLOUR))
        thing.modify(-1)
        return True
    elif thing.itemId == ITEM_FLOUR and onThing.type == TYPE_WATER:
        creature.addItem(Item(ITEM_DOUGH))
        onThing.type = TYPE_EMPTY
        thing.modify(-1)
        return True
    elif thing.itemId == ITEM_DOUGH and onThing.itemId in OVEN_ON:
        creature.addItem(Item(ITEM_BREAD))
        thing.modify(-1)
        return True
    return False
