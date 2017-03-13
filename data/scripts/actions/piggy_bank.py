BROKEN_PIGGY_BANK = 2115

@register("use", 2114)
def onUse(creature, thing, position, **k):
    if random.randint(1, 4) != 1:
        creature.magicEffect(EFFECT_POFF)
        creature.addItem(Item(2148, 1))
        thing.transform(BROKEN_PIGGY_BANK)
    else:
        creature.magicEffect(EFFECT_SOUND_YELLOW)
        creature.addItem(Item(2152, 1))
    return True