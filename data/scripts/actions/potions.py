POTIONS = {\
8704: {"empty": 7636, "splash": 5, "health": [50, 100]}, # small health potion
7618: {"empty": 7636, "splash": 5, "health": [100, 200]}, # health potion
7588: {"empty": 7634, "splash": 5, "health": [200, 400], "level": 50, "vocations": [3, 4, 7, 8], "vocStr": "knights and paladins"}, # strong health potion
7591: {"empty": 7635, "splash": 5, "health": [500, 600], "level": 80, "vocations": [4, 8], "vocStr": "knights"}, # great health potion
8473: {"empty": 7635, "splash": 5, "health": [700, 750], "level": 130, "vocations": [4, 8], "vocStr": "knights"}, # ultimate health potion
 
7620: {"empty": 7636, "splash": 2, "mana": [70, 130]}, # mana potion
7589: {"empty": 7634, "splash": 2, "mana": [110, 190], "level": 50, "vocations": [1, 2, 3, 5, 6, 7], "vocStr": "sorcerers, druids and paladins"}, # strong mana potion
7590: {"empty": 7635, "splash": 2, "mana": [200, 300], "level": 80, "vocations": [1, 2, 5, 6], "vocStr": "sorcerers and druids"}, # great mana potion
 
8472: {"empty": 7635, "splash": 3, "health": [200, 400], "mana": [110, 190], "level": 80, "vocations": [3, 7], "vocStr": "paladins"} # great spirit potion
}

@register('useWith', POTIONS.keys())
def onUseWith(creature, thing, position, onThing, onPosition, **k):
    potion = POTIONS[thing.itemId]
    if not potion:
        return False

    if creature.hasCondition(CONDITION_EXHAUST):
        creature.exhausted()
        return False

    try:
        if (creature.data["level"] < potion["level"]) or (creature.getVocationId()) not in potion["vocations"]:
            creature.say(("Only %s of level %d or above may drink this fluid." % (potion["vocStr"], potion["level"])), MSG_SPEAK_MONSTER_SAY)
            return False
    except:
        pass

    if not onThing.isPlayer() or (not config.usableOnTarget and creature != onThing):
        if not config.splashable:
            return False

        splash = Item(FULLSPLASH)
        splash.fluidSource = potion["splash"]
        splash.place(onPosition)
        splash.decay()

        if position.x == 0xFFFF:
            if thing.count > 1:
                thing.count -= 1
            else:
                thing.modify(-1)
            creature.addItem(Item(potion["empty"], 1))
        else:
            thing.modify(-1)
            Item(potion["empty"], 1).place(position)
        return False

    try:
        mana = potion["mana"]
        if mana:
            onThing.modifyMana(int(round(random.randint(mana[0], mana[1]) * config.manaMultiplier)))
    except:
        pass

    try:
        health = potion["health"]
        if health:
            onThing.modifyHealth(int(round(random.randint(health[0], health[1]) * config.healthMultiplier)))
    except:
        pass

    magicEffect(onPosition, EFFECT_MAGIC_BLUE)

    if not config.realAnimation:
        onThing.say("Aaaah...", MSG_SPEAK_MONSTER_SAY)
    else:
        for tid in getPlayers(creature.position, (1, 1)):
            if tid.isPlayer():
                tid.say("Aaaah...", MSG_SPEAK_MONSTER_SAY)

    if position.x == 0xFFFF:
        if thing.count > 1:
            thing.count -= 1
        else:
            thing.modify(-1)
        creature.addItem(Item(potion["empty"], 1))
    else:
        thing.modify(-1)
        Item(potion["empty"], 1).place(position)

    creature.condition(Condition(CONDITION_EXHAUST, 0, config.exhaust))

