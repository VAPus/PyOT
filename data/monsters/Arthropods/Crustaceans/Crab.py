crab = genMonster("Crab", 112, 6039)
crab.targetChance(10)
crab.type("blood")
crab.health(55)
crab.experience(30)
crab.speed(200) #correct
crab.walkAround(1,1,0) # energy, fire, poison
crab.behavior(summonable=305, hostile=True, illusionable=True, convinceable=305, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
crab.immunity(0,0,0) # paralyze, invisible, lifedrain
crab.defense(31, fire=1.1, earth=0, energy=1.1, ice=0.8, holy=1.0, death=1.0, physical=1.0, drown=0)
crab.loot( ("fish", 20.5), (2148, 100, 10), ("crab pincers", 19.25) )

crab.melee(20)