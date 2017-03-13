fishWater = 4608, 4609, 4610, 4611, 4612, 4613, 4614, 4615, 4616
nofishWater = 493, 4617, 4618, 4619, 4210, 4621, 4622, 4623, 4624, 4625, 4820, 4821, 4822, 4823, 4824, 4825
iceHoleFish = 7236

nail = 8309
worm =3976
fish =2667
mechanicalFish =10224
greenPerch = 7159
rainbowTrout = 7158
waterElementCorpse = 10499

fishingRods = 2580, 10223
mechanicalFishingRod = 10223
@register("useWith", fishingRods)
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    if onPosition.x == 0xFFFF:
        creature.notPossible()
        return

    if onThing.itemId in nofishWater:
        magicEffect(onPosition, EFFECT_LOSENERGY)
        return

    if onThing.itemId == waterElementCorpse:
        creature.message("Not supported yet")

        return

    formula = (creature.getActiveSkill(SKILL_FISH) / 200.0) + (0.85 * random.random())
    if thing.itemId == mechanicalFishingRod:
        useItem = creature.findItemById(nail, 1)
    else:
        useItem = creature.findItemById(worm, 1)
    if not useItem:
        return

    if onThing.itemId in fishWater:
        if formula > 0.7:
            if thing.itemId == mechanicalFishingRod:
                addfish = mechanicalFish
            else:
                addfish = fish

            try:
                creature.addItem(Item(addfish))
            except:
                pass

            onThing.transform(onThing.itemId+9)
            creature.skillAttempt(SKILL_FISH)
    elif onThing.itemId == iceHoleFish:
        if thing.itemId == mechanicalFishingRod:
            if formula > 0.5:
                addfish = mechanicalFish
        else:
            if formula > 0.83:
                addfish = rainbowTrout
            elif formula > 0.75:
                addfish = rainbowTrout
            elif formula > 0.5:
                addfish = greenPerch
            elif formula > 0.47:
                addfish = fish
    
        try:
            creature.addItem(Item(addfish))
        except:
            pass

        onThing.transform(onThing.itemId+1)
        creature.skillAttempt(SKILL_FISH, 2)

    onThing.decay(onPosition)
            
