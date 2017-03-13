instant = spell.Spell("Challenge", "exeta res", icon=93, group=SUPPORT_GROUP)
instant.require(mana=30, level=20, maglevel=0, learned=0, vocations=(8,))
instant.area(AREA_SQUARE)
instant.cooldowns(2, 3)
instant.targetEffect() # TODO
instant.effects(area=EFFECT_MAGIC_RED)