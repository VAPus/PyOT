Rabbit = genMonster("Rabbit", 74, 6017)
Rabbit.targetChance(0)
Rabbit.type("blood")
Rabbit.health(15)
Rabbit.experience(0)
Rabbit.speed(180) #correct
Rabbit.walkAround(1,1,1) # energy, fire, poison
Rabbit.behavior(summonable=220, hostile=False, illusionable=True, convinceable=220, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=15)
Rabbit.immunity(0,0,0) # paralyze, invisible, lifedrain
Rabbit.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Rabbit.loot( ("meat", 86.5, 2), ("carrot", 9.25) )