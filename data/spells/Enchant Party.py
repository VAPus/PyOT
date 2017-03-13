instant = spell.Spell("Enchant Party", "utori mas sio", icon=129, group=SUPPORT_GROUP)
instant.require(mana=120, level=32, maglevel=0, learned=0, vocations=(5,))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO