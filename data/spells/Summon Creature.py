instant = spell.Spell("Summon Creature", "utevo res", icon=9, group=SUPPORT_GROUP)
instant.require(mana=0, level=25, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO