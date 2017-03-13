instant = spell.Spell("Sharpshooter", "utito tempo san", icon=135, group=SUPPORT_GROUP)
instant.require(mana=450, level=60, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(2, 10)
instant.targetEffect() # TODO
instant.effects() # TODO