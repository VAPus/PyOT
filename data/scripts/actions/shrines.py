SMALL_SAPPHIRE  = 2146
SMALL_RUBY      = 2147
SMALL_EMERALD   = 2149
SMALL_AMETHYST  = 2150

ENCHANTED_SMALL_SAPPHIRE = 7759
ENCHANTED_SMALL_RUBY     = 7760
ENCHANTED_SMALL_EMERALD  = 7761
ENCHANTED_SMALL_AMETHYST = 7762

HOTA_WEAK = 2342
HOTA_FULL = 2343

SHRINES = {\
# Fire Shrine
SMALL_RUBY: (7504, 7505, 7506, 7507),\

# Ice Shrine
SMALL_SAPPHIRE: (7508, 7509, 7510, 7511),\

# Energy Shrine
SMALL_AMETHYST: (7512, 7513, 7514, 7515),\

# Earth Shrine
SMALL_EMERALD: (7516, 7517, 7518, 7519)\
}

ENCHANTED_GEMS = {\
SMALL_SAPPHIRE: ENCHANTED_SMALL_SAPPHIRE,
SMALL_RUBY: ENCHANTED_SMALL_RUBY,
SMALL_EMERALD: ENCHANTED_SMALL_EMERALD,
SMALL_AMETHYST: ENCHANTED_SMALL_AMETHYST
}

@register("useWith", (2146, 2147, 2149, 2150))
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if onThing.itemId == HOTA_WEAK and thing.itemId == SMALL_RUBY:
        thing.modify(-1)
        onThing.transform(HOTA_FULL)
        magicEffect(onPosition, EFFECT_MAGIC_RED)
        return True
    
    if onThing.itemId in SHRINES[thing.itemId] == False:
        return False
    
    count = thing.type != 0 and thing.type or 1
    manaCost = 300 * count
    soulCost = 2 * count
    requiredLevel = 30
    
    if creature.data["level"] < requiredLevel:
        creature.notEnough('level')
        return True
    
    # TODO: Some flag check here.
    """if creature.isPremium() == False:
        creature.needPremium()
        return True"""
    
    if creature.data["mana"] < manaCost:
        creature.notEnough('mana')
        return True
    
    if creature.data["soul"] < soulCost:
        creature.notEnough('soul')
        return True
    
    creature.modifyMana(-manaCost)
    creature.modifySoul(-soulCost)
    
    thing.count = count
    thing.transform(ENCHANTED_GEMS[thing.itemId])
    
    return True
