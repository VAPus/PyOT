instant = spell.Spell("Great Energy Beam", "exevo gran vis lux", icon=23, group=ATTACK_GROUP)
instant.require(mana=110, level=29, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(6, 2)
instant.area(AREA_BEAM7)
instant.targetEffect(callback=spell.damage(3.6, 6, 22, 37, ENERGY))
instant.effects(area=EFFECT_ENERGYAREA) #this or energy beam may have the wrong effect