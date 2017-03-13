shaburak_prince = genMonster("Shaburak Prince", 418, 5980)#corpse
shaburak_prince.health(2600, healthmax=2600)
shaburak_prince.type("blood")
shaburak_prince.defense(armor=33, fire=1, earth=1.3, energy=0.5, ice=0.5, holy=1, death=1, physical=1, drown=1)#
shaburak_prince.experience(1700)
shaburak_prince.speed(300)#
shaburak_prince.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
shaburak_prince.walkAround(energy=0, fire=0, poison=0)
shaburak_prince.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
shaburak_prince.voices("GREEN IS MEAN!", "WE RULE!", "POWER TO THE SHABURAK!", "DEATH TO THE ASKARAK!", "ONLY WE ARE TRUE DEMONS!")
shaburak_prince.melee(320)
shaburak_prince.loot( (2148, 100, 167), ("strong mana potion", 19.0), ("platinum coin", 89.0, 4), ("strong health potion", 13.75), ("brown mushroom", 5.0), ("stealth ring", 6.5), ("butcher's axe", 0.75), ("small ruby", 42.25, 5), ("bullseye potion", 0.75) )