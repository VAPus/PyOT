# bad
Thornfire_Wolf = genMonster("Thornfire Wolf", 414, 6079) # unkown yet
Thornfire_Wolf.targetChance(10)
Thornfire_Wolf.type("blood")
Thornfire_Wolf.health(600)
Thornfire_Wolf.experience(200)
Thornfire_Wolf.speed(200) #incorrect
Thornfire_Wolf.walkAround(1,0,1) # energy, fire, poison
Thornfire_Wolf.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Thornfire_Wolf.immunity(0,0,0) # paralyze, invisible, lifedrain
Thornfire_Wolf.defense(20, fire=0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0) 
Thornfire_Wolf.melee(65)#or more