instant = spell.Spell("Recovery", "utura", icon=159, group=HEALING_GROUP)
instant.require(mana=75, level=50, maglevel=0, learned=0, vocations=(4, 8, 3, 7))
instant.cooldowns(60, 1)
instant.targetEffect() # TODO
instant.effects() # TODO