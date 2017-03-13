chicken = genMonster("Chicken", 111, 6042)
chicken.type("blood")
chicken.health(15)
chicken.experience(0)
chicken.targetChance(10)
chicken.speed(200) #Incorrect
chicken.walkAround(1,1,1) # energy, fire, poison
chicken.behavior(summonable=220, hostile=True, illusionable=True, convinceable=220, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
chicken.voices("Cluck Cluck", "Gokgoooook")
chicken.immunity(0,0,0) # paralyze, invisible, lifedrain
chicken.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
chicken.loot( ("chicken feather", 20.0, 3), (3976, 17.5, 3), ("meat", 2.25), ("egg", 1.25) )