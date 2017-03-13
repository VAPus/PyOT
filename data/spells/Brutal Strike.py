instant = spell.Spell("Brutal Strike", "exori ico", icon=61, group=ATTACK_GROUP)
instant.require(mana=30, level=16, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(6, 2)
instant.range(4)
instant.targetEffect() # TODO
instant.effects() # TODO