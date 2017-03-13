import copy
lockers = (2589, 2590, 2591, 2592)
depot_id = 2594
@registerFirst('use', depot_id) # We got to register it first so we call it before container open
def openDepot(creature, thing, **k):
    if thing.depotId == None:
        # Aga, no locker id.
        creature.lmessage("It would appear this locker has no keyhole.")
        return False
    if thing.owners and creature not in thing.owners:
        creature.lmessage("This depot box is already in use by someone else")
        return False
        
    
    thing.owners = [creature]
    if thing.depotId in creature.depot:
        thing.container = creature.depot[thing.depotId]
        for item in thing.container:
            item.inContainer = thing

@register('close', depot_id)
def closeDepot(creature, thing, **k):
    if thing.depotId != None:
        creature.depot[thing.depotId] = copy.deepcopy(thing.container)
        thing.container = []
        thing.owners = []

@registerFirst('use', lockers)
def openLocker(creature, thing, **k):
    depot = Item(depot_id)
    depot.depotId = thing.depotId
    thing.containerSize = 3
    thing.container = [depot, Item(2334)]
    
