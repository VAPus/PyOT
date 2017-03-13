# Autoconverted script for PyOT
# Untested. Please remove this message when the script is working properly!

ITEMS = [9010,11337,7441,7442,7444,7445]

SKINS = {
# Minotaurs
2830: [25000, 5878],
2871: [25000, 5878],
2866: [25000, 5878],
2876: [25000, 5878],
3090: [25000, 5878],

# Low Class Lizards
4259: [25000, 5876],
4262: [25000, 5876],
4256: [25000, 5876],

# High Class Lizards
11288: [25000, 5876],
11280: [25000, 5876],
11272: [25000, 5876],
11284: [25000, 5876],

# Dragons
3104: [25000, 5877],
2844: [25000, 5877],

# Dragon Lords
2881: [25000, 5948],

# Behemoths
2931: [ [ 10000, 5930 ], [ 35000, 5893 ] ],

# Bone Beasts
3031: [25000, 5925],

# The Mutated Pumpkin
8961: [ [ 5000, 7487 ], [ 10000, 7737 ], [ 20000, 6492 ], [ 30000, 8860 ], [ 45000, 2683 ], [ 60000, 2096 ], [ 90000, 9005, 50 ] ]
}

@register("useWith", 5908)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    skin = SKINS[onThing.itemId]
    if (skin == None) or (onThing.itemId not in ITEMS):
        creature.notPossible()
        return True

    if isInArray(ITEMS,onThing.itemId):
        if onThing.itemId == 9010:
            if getPlayerStorageValue(creature, 65049) <= 0:
                magicEffect(onPosition, EFFECT_MAGIC_GREEN)
                creature.addItem(Item(8310, 1))
                setPlayerStorageValue(creature, 65049, 1)
            else:
                doCreatureSayWithRadius(creature, "You already used your knife on the corpse.", 'MSG_SPEAK_MONSTER_SAY', 1, 1)
        elif onThing.itemId == 11337: #piece of marble rock
            statue = random.randint(1, 100)
            if statue <= 70:
                doItemSetAttribute(onThing, "description", "This shoddy work was made by %s.", creature.name())
                onThing.transform(11338, position) #rough
            elif statue <= 99:
                doItemSetAttribute(onThing, "description", "This little figurine made by %s has some room for improvement.", creature.name())
                onThing.transform(11339, position) #regular
            else:
                doItemSetAttribute(onThing, "description", "This little figurine of Tibiasula was masterfully sculpted by %s.", creature.name())
                onThing.transform(11340, position) #beautiful
        elif onThing.itemId == 7441: #ice cube
            if random.randint(1, 100) <= 30: #30%
                onThing.transform(7442, position) #1 carve
            else:
                doPlayerSendDefaultCancel(creature, "You broke the ice cube")
                creature.removeItem(onPosition, onStackpos)
        elif onThing.itemId == 7442: #ice cube, 1 carve
            if random.randint(1, 100) <= 20: #20%
                onThing.transform(7444, position) #2 carve
            else:
                doPlayerSendDefaultCancel(creature, "You broke the ice cube")
                creature.removeItem(onPosition, onStackpos)
        elif onThing.itemId == 7444: #ice cube, 2 carve
            if random.randint(1, 100) <= 10: #10%
                onThing.transform(7445, position) #3 carve
            else:
                doPlayerSendDefaultCancel(creature, "You broke the ice cube")
                creature.removeItem(onPosition, onStackpos)
        elif onThing.itemId == 7445: #ice cube, 3 carve
            if random.randint(1, 100) <= 5: #5%
                onThing.transform(7446, position) #ice mammoth
            else:
                doPlayerSendDefaultCancel(creature, "You broke the ice cube")
                creature.removeItem(onPosition, onStackpos)
        magicEffect(onPosition, EFFECT_BLOCKHIT)
    else:
        random, effect, transform = random.randint(1, 100000), EFFECT_MAGIC_GREEN, True
        if type(skin[1]) == 'table':
            added = True
            for _skin in range(skin):
                if random <= _skin[1]:
                    doPlayerAddItem(creature, _skin[2], _skin[3] or 1)
                    added = True
                    break

            if not added and onThing.itemId == 8961:
                effect = EFFECT_POFF
                transform = True
        elif random <= skin[1]:
            doPlayerAddItem(creature, skin[2], skin[3] or 1)
        else:
            effect = EFFECT_POFF

        magicEffect(onPosition, effect)
        if transform:
            onThing.transform(onThing.itemId + 1, position)

    return True


