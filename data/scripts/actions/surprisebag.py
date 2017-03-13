# Autoconverted script for PyOT
# Untested. Please remove this message when the script is working properly!

PRESENT_BLUE = [2687, 6394, 6280, 6574, 6578, 6575, 6577, 6569, 6576, 6572, 2114]
PRESENT_RED = [2152, 2152, 2152, 2153, 5944, 2112, 6568, 6566, 2492, 2520, 2195, 2114, 2114, 2114, 6394, 6394, 6576, 6576, 6578, 6578, 6574, 6574]

@register("use", (6570, 6571))
def onUse(creature, thing, position, **k):
    count = 1
    if thing.itemId == 6570:
        randomChance = random.randint(0, len(PRESENT_BLUE)-1)
        if randomChance == 1:
            count = 10
        elif randomChance == 2:
            count = 3
        creature.addItem(Item(PRESENT_BLUE[randomChance], count))
    elif thing.itemId == 6571:
        randomChance = random.randint(0, len(PRESENT_RED)-1)
        if randomChance > 0 and randomChance < 4:
            count = 10
        creature.addItem(Item(PRESENT_RED[randomChance], count))
    
    magicEffect(position, EFFECT_GIFT_WRAPS)
    creature.removeItem(thing)
    return True
