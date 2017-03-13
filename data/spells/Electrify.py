instant = spell.Spell("Electrify", "utori vis", icon=140, group=ATTACK_GROUP)
instant.require(mana=30, level=34, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(30, 2)
instant.targetEffect() # TODO
instant.effects() # TODO