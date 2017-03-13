undead_dragon = genMonster("Undead Dragon", 231, 6306)
undead_dragon.health(8350, healthmax=8350)
undead_dragon.type("undead")
undead_dragon.defense(armor=73, fire=0, earth=0, energy=1, ice=0.5, holy=1.25, death=0, physical=0.95, drown=1)
undead_dragon.experience(7200)
undead_dragon.speed(300)
undead_dragon.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=500)
undead_dragon.walkAround(energy=1, fire=0, poison=0)
undead_dragon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
undead_dragon.voices("FEEEED MY ETERNAL HUNGER!", "I SENSE LIFE")
undead_dragon.loot( ("great health potion", 10.75), ("power bolt", 26.5, 6), ("demonic essence", 12.75, 3), ("royal helmet", 1.0), ("broadsword", 40.75), ("unholy bone", 63.0), ("torn book", 28.25), ("platinum coin", 100, 5), ("onyx arrow", 100, 10), ("soul orb", 15.25), ("blank rune", 32.75, 2), (2148, 100, 265), ("divine plate", 0.5), ("golden mug", 4.0), ("death ring", 2.0), ("knight armor", 2.0), ("rusty armor", 1.0), ("gold ingot", 0.5), ("dragonbone staff", 1.0), ("life crystal", 0.75), ("war axe", 0.25), ("hardened bone", 0.5) )

#Poison Wave (150-690)--doesnt exist anymore?, Smoke Wave (makes you drown for 2 minutes) --doesnt exist anymore?, Envenom (0-180)--doesnt exist anymore?, Life Drain Exori --doesnt exist anymore?
udbbomb = spell.Spell("ud bbomb", target=TARGET_TARGETONLY)
udbbomb.area(AREA_CIRCLE3)
udbbomb.element(PHYSICAL) #?
udbbomb.effects(area=EFFECT_DRAWBLOOD) 

udpbomb = spell.Spell("ud pbomb", target=TARGET_TARGETONLY) #does this poison you too?
udpbomb.area(AREA_CIRCLE3)
udpbomb.element(EARTH)
udpbomb.effects(area=EFFECT_POISONAREA)

udldwave = spell.Spell("ud ldwave", target=TARGET_AREA)
udldwave.area(AREA_WAVE8)
udldwave.element(PHYSICAL) #life drain
udldwave.effects(area=EFFECT_MAGIC_RED)

udcwave = spell.Spell("ud cwave", target=TARGET_AREA) #makes you cursed
udcwave.area(AREA_WAVE8)
udcwave.effects(area=EFFECT_SMOKE) #?

undead_dragon.melee(480)
undead_dragon.selfSpell("Light Healing", 200, 250, check=chance(18))
undead_dragon.targetSpell("ud bbomb", 300, 400, check=chance(20))
undead_dragon.targetSpell("ud pbomb", 100, 390, check=chance(20))
undead_dragon.targetSpell("ud ldwave", 300, 700, check=chance(20))
undead_dragon.targetSpell(2268, 25, 600, check=chance(20)) #sd