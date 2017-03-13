askarak_lord = genMonster("Askarak Lord", 410, 5980)#corpse
askarak_lord.health(2100, healthmax=2100)
askarak_lord.type("blood")
askarak_lord.defense(armor=30, fire=1.3, earth=1, energy=0.5, ice=0.5, holy=1, death=1, physical=1, drown=1)#
askarak_lord.experience(1200)
askarak_lord.speed(300)#
askarak_lord.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
askarak_lord.walkAround(energy=0, fire=0, poison=0)
askarak_lord.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
askarak_lord.voices("DEATH TO THE SHABURAK!", "ONLY WE ARE TRUE DEMONS!", "GREEN WILL RULE!", "RED IS MAD")
askarak_lord.melee(200)#
askarak_lord.loot( ("small emerald", 9.0, 4), ("springsprout rod", 0.75), ("energy ring", 2.0), ("magic sulphur", 1.5), ("strong health potion", 7.0), ("brown mushroom", 8.25), ("strong mana potion", 7.5), ("platinum coin", 62.75, 2), (2148, 100, 181) )