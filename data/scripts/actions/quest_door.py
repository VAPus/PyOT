doors = 1223, 1225, 1241, 1243, 1255, 1257, 3542, 3551, 5105, 5114, 5123, 5132, 5288, 5290, 5745, 5748, 6202, 6204, 6259, 6261, 6898, 6907,\
        7040, 7049, 8551, 8553, 9175, 9177, 9277, 9279, 10278, 10475, 10484, 10791


@register('use', doors)
def openDoor(creature, thing, position, **k):
    if not thing.actionIds():
        thing.transform(thing.itemId+1)
        return

    canEnter = True
    for action in thing.actionIds():
        if not creature.getStorage(action):
            canEnter = False

    if not canEnter:
        creature.lmessage("The door is sealed against unwanted intruders.")
    
    thing.transform(thing.itemId+1)