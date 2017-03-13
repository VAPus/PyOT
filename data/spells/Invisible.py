instant = spell.Spell("Invisibile", "utana vid", icon=45, group=SUPPORT_GROUP)
instant.require(mana=440, level=35, maglevel=0, learned=0, vocations=(1, 2, 5, 6))
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects() # TODO