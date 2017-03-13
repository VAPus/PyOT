instant = spell.Spell("Creature Illusion", "utevo res ina", icon=38, group=SUPPORT_GROUP)
instant.require(mana=100, level=23, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO