#mostly unknown
draptor = genMonster("Draptor", 8, 5980)
draptor.health(3000)
draptor.type("blood")
draptor.defense(armor=2, fire=1, earth=1, energy=0, ice=1, holy=1, death=1, physical=1, drown=1)#
draptor.experience(2400)
draptor.speed(300)
draptor.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=1500)
draptor.walkAround(energy=0, fire=0, poison=0)
draptor.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
#draptor.voices(*arg)
draptor.loot( (2148, 100, 180), ("strong mana potion", 13.25), ("strong health potion", 21.0), ("draptor scales", 5.25) )

dfwave = spell.Spell("drap fwave", target=TARGET_AREA)
dfwave.area(AREA_WAVE6)
dfwave.element(FIRE)
dfwave.effects(area=EFFECT_HITBYFIRE) #wrong effect

deb = spell.Spell("drap eberserk")
deb.area(AREA_SQUARE)
deb.element(ENERGY)
deb.effects(target=EFFECT_PURPLEENERGY, area=EFFECT_YELLOWENERGY)

#plays a red music note when it hastes
#energy hit. is it only does from close like a demon?

draptor.melee(150)
draptor.selfSpell("Light Healing", 100, 150, check=chance(18)) #unknown healing
draptor.targetSpell("drap fwave", 130, 200, check=chance(5)) #unknown damage
draptor.targetSpell("drap eberserk", 130, 200, check=chance(5)) #unknown damage