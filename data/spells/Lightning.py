instant = spell.Spell("Lightning", "exori amp vis", icon=149, group=ATTACK_GROUP)
instant.require(mana=160, level=55, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(8, 2)
instant.range(4)
instant.area(AREA_WAVE1)
instant.targetEffect(callback=spell.damage(2.2, 3.4, 12, 21, ENERGY))
instant.effects() # TODO