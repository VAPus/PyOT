instant = spell.Spell("Magic Shield", "utamo vita", icon=44, group=SUPPORT_GROUP)
instant.require(mana=50, level=14, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO