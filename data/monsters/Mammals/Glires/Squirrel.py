Squirrel = genMonster("Squirrel", 274, 7628)
Squirrel.targetChance(0)
Squirrel.type("blood")
Squirrel.health(20)
Squirrel.experience(0)
Squirrel.speed(200) #incorrect
Squirrel.walkAround(1,1,1) # energy, fire, poison
Squirrel.behavior(summonable=220, hostile=False, illusionable=True, convinceable=220, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=20)
Squirrel.voices("Chchch")
Squirrel.immunity(0,0,0) # paralyze, invisible, lifedrain
Squirrel.defense(1, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Squirrel.loot( ("acorn", 51.25), ("walnut", 0.5), ("peanut", 1.5) )
