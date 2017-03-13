instant = spell.Spell("Find Person", "exiva", icon=20, group=SUPPORT_GROUP)
instant.require(mana=20, level=8, maglevel=0, learned=0, vocations=(1, 2, 3, 4, 5, 6, 7, 8))
instant.cooldowns(2, 3)
#instant.targetEffect() # TODO there is no target
instant.effects() # TODO