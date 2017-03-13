instant = spell.Spell("Protector", "utamo tempo", icon=132, group=SUPPORT_GROUP)
instant.require(mana=200, level=55, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(2, 10)
instant.targetEffect() # TODO
instant.effects() # TODO