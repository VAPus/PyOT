ITEM_PRE_WHEAT = 2739
ITEM_WHEAT = 2737
ITEM_BUNCH_WHEAT = 2694
ITEM_PRE_SUGAR_CANE = 5471
ITEM_SUGAR_CANE = 5463
ITEM_BUNCH_SUGAR_CANE = 5467

#sugar can is really cut with a sickle but for now a scythe is good.

@register("useWith", 2550)
def onUseWith(onThing, onPosition, **k):
    if onThing.itemId == ITEM_PRE_WHEAT:
        onThing.transform(ITEM_WHEAT)
        Item(ITEM_BUNCH_WHEAT, 1).place(onPosition)
    elif onThing.itemId == ITEM_PRE_SUGAR_CANE:
        onThing.transform(ITEM_SUGAR_CANE)
        Item(ITEM_BUNCH_SUGAR_CANE, 1).place(onPosition)
    else:
        return False
    onThing.decay()
    return True