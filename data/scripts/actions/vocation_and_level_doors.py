doors = 1227, 1229, 1245, 1247, 1259, 1261, 3540, 3549, 5103, 5112, 5121, 5130, 5292, 5294, 6206, 6208, 6263, 6265, 6896, 6905, 7038, 7047, 8555,\
        8557, 9179, 9181, 9281, 9283, 10280, 10282, 10284, 10473, 10482

@register('use', doors)
def openDoor(creature, thing, position, **k):
    if not thing.actionIds():
        thing.transform(thing.itemId+1)
        return

    canEnter = True
    for action in thing.actionIds():
        if action > 1000 and action < 2000:
            if not creature.data["level"] > action-1000:
                canEnter = False
                break
        elif action > 2000 and action < 2010:
            if not creature.vocation == action-2000:
                canEnter = False
                break

    if not canEnter:
        creature.lmessage("Only the worthy may pass.")
    
    thing.transform(thing.itemId+1)