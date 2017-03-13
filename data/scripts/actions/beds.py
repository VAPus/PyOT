def useBed(creature, thing, position, **k):
    if not thing.owners:
        creature.cancelMessage("Not possible. Noone owns this bed.")
        return

    elif not creature.clientId() in thing.owners:
        creature.cancelMessage("Not possible. You don't own this bed.")

    # First grab the sex of the player.
    sex = creature.data['sex']
    transformTo = 0
    if sex == MALE:
        transformTo = thing.maleTransformTo
    elif sex == FEMALE:
        transformTo = thing.femaleTransformTo

    thing.transform(transformTo)

    # Set a storage value.
    creature.setStorage("inBed", (time.time(), position.x, position.y, position.z, position.instanceId))

    # Logout the player.
    creature.logout()    

@register("login")
def onLogin(creature, **k):
    inBed = creature.getStorage('inBed')
    if inBed:
        timeInBed = time.time() - inBed[0]
        bedPosition = Position(inBed[1], inBed[2], inBed[3], inBed[4])
        
        # Find the bed to transform it back.
        tile = bedPosition.getTile()
        for item in tile.getItems():
            if item.partnerDirection != None:
                # It's the bed.
                item.setPosition(bedPosition)
                item.transform(item.transformTo)
                break

        creature.removeStorage("inBed")

        # Do some magic with timeInBed. Like offline training here.
        # Not for alpha1.
        """if config.offlineTraining and timeInBed >= config.offlineTrainingMinimumSleep:
             trainingTime = min(timeInBed, config.offlineTrainingMaximumSleep)
        """

        # TODO: Also hp/mana regen, souls.

registerForAttr('use', 'maleTransformTo', useBed)

