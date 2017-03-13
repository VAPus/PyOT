instant = spell.Spell("Cancel Invisibility", "exana ina", icon=90, group=SUPPORT_GROUP)
instant.require(mana=200, level=26, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(2, 3)
instant.area(AREA_CIRCLE3)
instant.targetEffect() # TODO
instant.effects(area=EFFECT_MAGIC_BLUE)