@register("useWith", 2600)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    rand = random.randint(1, 2)
    if onThing.itemId == 7528:
        onThing.transform(7529)
    elif onThing.itemId == 7529:
        if rand == 1:
            onThing.transform(7530)
        elif rand == 2:
            onThing.transform(7531)
    elif onThing.itemId == 7530:
        if rand == 1:
            onThing.transform(7532)
        elif rand == 2:
            onThing.transform(7533)
    elif onThing.itemId == 7532:
        if rand == 1:
            onThing.transform(7534)
        elif rand == 2:
            onThing.transform(7535)
    
    return True
