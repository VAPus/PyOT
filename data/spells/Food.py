instant = spell.Spell("Food", "exevo pan", icon=42, group=SUPPORT_GROUP)
instant.require(mana=120, level=14, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(0, 3)
instant.targetEffect() # TODO
instant.effects() # TODO