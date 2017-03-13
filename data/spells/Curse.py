instant = spell.Spell("Curser", "utori mort", icon=139, group=ATTACK_GROUP)
instant.require(mana=30, level=75, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(50, 2)
instant.targetEffect() # TODO
instant.effects() # TODO