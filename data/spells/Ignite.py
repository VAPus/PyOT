instant = spell.Spell("Ignite", "utori flam", icon=138, group=ATTACK_GROUP)
instant.require(mana=30, level=26, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(30, 2)
instant.targetEffect() # TODO
instant.effects() # TODO