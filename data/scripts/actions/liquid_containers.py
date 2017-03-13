"""
XXX: Broken.
containers = 2005

@register('useWith', containers)
def onUse(creature, thing, position, onThing, **k):
    print thing.itemId
    print onThing.itemId
    if not thing.type and onThing.type:
        thing.type = onThing.type
    creature.removeItem(position)
    creature.addItem(thing)
"""