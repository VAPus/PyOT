instant = spell.Spell("Berserk", "exori", icon=80, group=ATTACK_GROUP)
instant.require(mana=115, level=35, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(4, 2)
instant.area(AREA_SQUARE)
instant.targetEffect(callback=spell.meleeBased(1, 1, 0.5, 1.5, PHYSICAL)) #Constants taken from http://tibia.wikia.com/wiki/Formula
instant.effects(area=EFFECT_HITAREA)