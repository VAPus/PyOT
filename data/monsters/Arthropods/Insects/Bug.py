bug = genMonster("Bug", 45, 5990)
bug.type("slime")
bug.health(29)
bug.experience(18)
bug.targetChance(10)
bug.speed(160) #correct
bug.walkAround(1,1,1) # energy, fire, poison
bug.behavior(summonable=250, hostile=True, illusionable=True, convinceable=250, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
bug.immunity(0,0,0) # paralyze, invisible, lifedrain
bug.defense(2, fire=1.1, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
bug.loot( ("cherry", 5.5, 3), (2148, 100, 6) )
bug.melee(23)