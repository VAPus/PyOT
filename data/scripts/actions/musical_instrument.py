instruments = {2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2332, 2364, 2367, 2368, 2370, 2371, 2372, 2373, 2374, 3951, 3953, 3957}

birdCage = 2095
woodenWhistle = 5786
didgeridoo = 3952
cornucopia = 2369
partyTrumpet = 6572
usedPartyTrumpet = 6573

extras = {birdCage, woodenWhistle, didgeridoo, cornucopia, partyTrumpet}

@register("use", extras|instruments)
def onUse(creature, thing, position, **k):
    chance = random.randint(1,5)

    if thing.itemId in instruments:
        magicEffect(position, EFFECT_SOUND_BLUE)
    elif thing.itemId == birdCage:
        magicEffect(position, EFFECT_SOUND_YELLOW)
    elif thing.itemId == didgeridoo and chance == 1:
        magicEffect(position, EFFECT_SOUND_BLUE)
    elif thing.itemId == partyTrumpet:
        thing.transform(usedPartyTrumpet)
        creature.say("TOOOOOOT!", 'MSG_SPEAK_MONSTER_SAY')
        magicEffect(position, EFFECT_SOUND_BLUE)
        thing.decay()
    elif thing.itemId == cornucopia:
        for i in range(0, 10):
            creature.addItem(game.item.Item(2681))

        thing.transform(0)
        creature.magicEffect(EFFECT_SOUND_YELLOW, position)

    elif thing.itemId == woodenWhistle:
        if chance == 2:
            magicEffect(position, EFFECT_SOUND_RED)
        else:
            creature.magicEffect(EFFECT_SOUND_PURPLE)
            summonCreature("Wolf", creature.positionInDirection(NORTH))
            