instant = spell.Spell("Train Party", "utito mas sio", icon=126, group=SUPPORT_GROUP)
instant.require(mana=60, level=32, maglevel=0, learned=0, vocations=(8,))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO