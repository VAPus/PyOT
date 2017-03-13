shaburak_lord = genMonster("Shaburak Lord", 409, 5980)#corpse
shaburak_lord.health(2100, healthmax=2100)
shaburak_lord.type("blood")
shaburak_lord.defense(armor=30, fire=1, earth=1.3, energy=0.5, ice=0.5, holy=1, death=1, physical=1, drown=1)#
shaburak_lord.experience(1200)
shaburak_lord.speed(300)#
shaburak_lord.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
shaburak_lord.walkAround(energy=0, fire=0, poison=0)
shaburak_lord.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
shaburak_lord.voices("GREEN IS MEAN!", "WE RULE!", "POWER TO THE SHABURAK!", "DEATH TO THE ASKARAK!", "ONLY WE ARE TRUE DEMONS!")
shaburak_lord.melee(200)#
shaburak_lord.loot( ("brown mushroom", 6.25), (2148, 100, 162), ("strong health potion", 8.25), ("platinum coin", 59.75, 2), ("steel boots", 0.5), ("small ruby", 16.75, 5), ("strong mana potion", 6.25), ("energy ring", 1.0), ("magma coat", 0.5), ("magic sulphur", 1.5), ("wand of inferno", 0.5) )
