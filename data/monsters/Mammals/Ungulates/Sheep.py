Sheep = genMonster("Sheep", 14, 5991)
Sheep.targetChance(0)
Sheep.type("blood")
Sheep.health(20)
Sheep.experience(0)
Sheep.speed(200) #incorrect
Sheep.walkAround(1,1,1) # energy, fire, poison
Sheep.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=20)
Sheep.voices("Maeh")
Sheep.immunity(0,0,0) # paralyze, invisible, lifedrain
Sheep.defense(2, fire=1.1, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Sheep.loot( ("meat", 67.5, 4), ("wool", 1.5) )