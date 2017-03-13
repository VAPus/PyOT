cockroach = genMonster("Cockroach", 284, 8593)
cockroach.targetChance(0)
cockroach.type("slime")
cockroach.health(1)
cockroach.experience(0)
cockroach.speed(200) #incorrect
cockroach.walkAround(1,1,1) # energy, fire, poison
cockroach.behavior(summonable=200, hostile=False, illusionable=True, convinceable=200, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=1)
cockroach.immunity(0,0,0) # paralyze, invisible, lifedrain
cockroach.defense(0, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
cockroach.loot( ("cockroach leg", 100.0) )