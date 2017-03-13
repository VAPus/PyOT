instant = spell.Spell("Ultimate Light", "utevo vis lux", icon=75, group=SUPPORT_GROUP)
instant.require(mana=140, level=26, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO