# First use of actions :p
def container(creature, thing, position, index, **k):
    if thing.owners:
        party = creature.party()
        ownersParty = thing.owners[0].party()
        if creature not in thing.owners and (not party or party is not ownersParty): # Prevent people to open owned things. + Party features.
            return
    if thing.openIndex == None:
        # Open a bag inside a bag?
        open = True
        bagFound = creature.getContainer(index)
            
        if bagFound:
            print ("ok --", index)
            # Virtual close
            del creature.openContainers[index].openIndex
                
            # Virtual switch
            thing.openIndex = index
            thing.parent = creature.openContainers[index]
            
            # Virtual reopen
            creature.openContainers[index] = thing
            
            # Update the container
            creature.updateContainer(thing, parent=1)
            open = False
            ok = True
            
        if open:
            # Open a new one
            parent = 0

            #if position.x == 0xFFFF and position.y >= 64:
            if bagFound:
                parent = 1
                #thing.parent = creature.openContainers[position.y-64]
            
            try:
                thing.openCreatures.append(creature)
            except:
                thing.openCreatures = [creature]
            ok = creature.openContainer(thing, parent=parent)

        # Opened from ground, close it on next step and set openCreatures :)
        if ok:
            def _verifyClose(who):
                if thing.openIndex != None:
                    if not thing.position or not who.inRange(thing.position, 1, 1):
                        who.closeContainer(thing)
                    else:
                        who.scripts["onNextStep"].append(_verifyClose)
                    
            creature.scripts["onNextStep"].insert(0, _verifyClose)
    else:
        creature.closeContainer(thing)

def containerMove(creature, thing, position, onPosition, **k):
    # Prevent this when dropping items INTO bags.
    if onPosition.x == 0xFFFF:
        return

    if thing.openCreatures and onPosition:
        for owner in thing.openCreatures[:]:
            if not owner.inRange(onPosition, 1, 1) or onPosition.z != owner.position.z:
                owner.closeContainer(thing)

registerForAttr('use', 'containerSize', container)
registerForAttr('dropOnto', 'containerSize', containerMove)
