Silver_Rabbit = genMonster("Silver Rabbit", 252, 7338)
Silver_Rabbit.targetChance(10)
Silver_Rabbit.type("blood")
Silver_Rabbit.health(15)
Silver_Rabbit.experience(0)
Silver_Rabbit.speed(184) #correct
Silver_Rabbit.walkAround(1,1,1) # energy, fire, poison
Silver_Rabbit.behavior(summonable=220, hostile=False, illusionable=True, convinceable=220, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=15)
Silver_Rabbit.immunity(0,0,0) # paralyze, invisible, lifedrain
Silver_Rabbit.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Silver_Rabbit.loot( ("silky fur", 30.75), ("meat", 84.0, 2), ("carrot", 8.25), ("coloured egg", 0.25) )