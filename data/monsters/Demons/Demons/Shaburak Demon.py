shaburak_demon = genMonster("Shaburak Demon", 417, 5980)#corpse
shaburak_demon.health(1500)
shaburak_demon.type("blood")
shaburak_demon.defense(armor=26, fire=1, earth=1.3, energy=0.5, ice=0.5, holy=1, death=1, physical=1, drown=1)#
shaburak_demon.experience(900)
shaburak_demon.speed(300)#
shaburak_demon.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
shaburak_demon.walkAround(energy=0, fire=0, poison=0)
shaburak_demon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
shaburak_demon.voices("GREEN IS MEAN!", "WE RULE!", "POWER TO THE SHABURAK!", "DEATH TO THE ASKARAK!", "ONLY WE ARE TRUE DEMONS!")
shaburak_demon.melee(140)
shaburak_demon.loot( (2148, 100, 252), ("wand of inferno", 0.5), ("small ruby", 15.0, 5), ("strong mana potion", 5.25), ("royal spear", 37.0, 6), ("energy ring", 1.25), ("strong health potion", 6.25), ("piggy bank", 1.0), ("brown mushroom", 3.25), ("bullseye potion", 0.25), ("magma legs", 0.0025), ("magic sulphur", 0.0025) )