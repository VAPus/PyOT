instant = spell.Spell("Heal Party", "utura mas sio", icon=128, group=SUPPORT_GROUP)
instant.require(mana=120, level=32, maglevel=0, learned=0, vocations=(6,))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO