cave_rat = genMonster("Cave Rat", 56, 5964)
cave_rat.type("blood")
cave_rat.health(30)
cave_rat.experience(10)
cave_rat.targetChance(10)
cave_rat.speed(150) # Correct
cave_rat.walkAround(1,1,1) # energy, fire, poison
cave_rat.behavior(summonable=250, hostile=True, illusionable=True, convinceable=250, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=3)
cave_rat.voices("Meep!", "Meeeeep!")
cave_rat.immunity(0,0,0) # paralyze, invisible, lifedrain
cave_rat.defense(2, fire=1.1, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
cave_rat.loot( ("cheese", 29.75), (2148, 100, 2), (3976, 14.5, 2), ("cookie", 1.0) )
cave_rat.melee(10)