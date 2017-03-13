#need to be able to light empty coal basins
#need too add hit effects when using it on the proper items

@register('useWith', 5468)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if onThing.itemId == 5466: # Sugar cane
        validItem = True
        onThing.transform(5465)
    elif onThing.itemId == 7538:
        validItem = True
        onThing.transform(7544)
    elif onThing.itemId == 7543: # Spider Webs
        validItem = True
        onThing.transform(7545)

    if validItem == True and random.randint(0,20) == 0:
        creature.modifyHealth(-5)
        magicEffect(position, EFFECT_EXPLOSIONAREA)
        creature.removeItem(position)

    else:
        return False