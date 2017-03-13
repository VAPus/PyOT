instant = spell.Spell("Annihilation", "exori gran ico", icon=62, group=ATTACK_GROUP)
instant.require(mana=300, level=110, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(30, 4)
instant.range(1) #?
instant.targetEffect() # TODO
instant.effects() # TODO