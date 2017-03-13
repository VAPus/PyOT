instant = spell.Spell("Inflict Wound", "utori kor", icon=141, group=ATTACK_GROUP)
instant.require(mana=30, level=40, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(30, 2)
instant.targetEffect() # TODO
instant.effects() # TODO