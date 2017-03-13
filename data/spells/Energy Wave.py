instant = spell.Spell("Energy Wave", "exevo vis hur", icon=13, group=ATTACK_GROUP)
instant.require(mana=170, level=38, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(8, 2)
instant.area(AREA_WAVE5)
instant.targetEffect(callback=spell.damage(4.5, 7.5, 20, 55, ENERGY))
instant.effects(area=EFFECT_ENERGYAREA) #might be the wrong effect