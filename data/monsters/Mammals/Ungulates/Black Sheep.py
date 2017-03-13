black_sheep = genMonster("Black Sheep", 13, 5994)
black_sheep.type("blood")
black_sheep.health(20)
black_sheep.experience(0)
black_sheep.targetChance(10)
black_sheep.speed(200) # speed incorrect
black_sheep.walkAround(1,1,1) # energy, fire, poison
black_sheep.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=20)
black_sheep.voices("Maeh")
black_sheep.immunity(0,0,0) # paralyze, invisible, lifedrain
black_sheep.defense(2, fire=1.1, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
black_sheep.loot( ("meat", 69.0, 5), ("black wool", 1.5) )