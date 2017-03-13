Pig = genMonster("Pig", 60, 6000)
Pig.targetChance(0)
Pig.type("blood")
Pig.health(25)
Pig.experience(0)
Pig.speed(200) #incorrect
Pig.walkAround(1,1,1) # energy, fire, poison
Pig.behavior(summonable=255, hostile=False, illusionable=True, convinceable=255, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=25)
Pig.voices("Oink oink", "Oink")
Pig.immunity(0,0,0) # paralyze, invisible, lifedrain
Pig.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Pig.loot( ("meat", 65.5, 4), ("pig foot", 1.25) )