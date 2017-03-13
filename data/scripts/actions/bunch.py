DISTILLERY = (5469, 5470, 5513, 5514)

@register("useWith", 5467)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    print ("____called")
    if onThing.itemId in DISTILLERY:
        if  not onThing.hasAction('DISTILLERY_FULL'):
            onThing.description = 'It is full.'
            onThing.addAction('DISTILLERY_FULL')
            thing.modify(-1)
        else:
            creature.cancelMessage('The machine is already full with bunches of sugar cane.')
        return True
    
    return False



