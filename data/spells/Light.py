instant = spell.Spell("Light", "utevo lux", icon=10, group=SUPPORT_GROUP)
instant.require(mana=20, level=8, maglevel=0, learned=0, vocations=(1, 2, 3, 4, 5, 6, 7, 8))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO