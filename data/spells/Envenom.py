instant = spell.Spell("Envenom", "utori pox", icon=142, group=ATTACK_GROUP)
instant.require(mana=30, level=50, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(40, 2)
instant.targetEffect() # TODO
instant.effects() # TODO