convert = {}
convert[2956] = (5905, EFFECT_MAGIC_BLUE) # Vampire dust
convert[2916] = (5906, EFFECT_MAGIC_RED) # Demon dust

@register("useWith", 5942)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if not isinstance(onThing, Item) or not onThing.itemId in convert:
        return

    if random.randint(1,15) == 1:
        try:
            creature.addItem(Item(convert[onThing.itemId][0]))
            magicEffect(onPosition, convert[onThing.itemId][1])
        except:
            creature.notPossible()
            return
    else:
        magicEffect(onPosition, EFFECT_BLOCKHIT)

    onThing.transform(onThing.itemId + 1)
