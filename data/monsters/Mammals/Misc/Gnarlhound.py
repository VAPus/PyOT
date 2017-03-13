Gnarlhound = genMonster("Gnarlhound", 341, 11250)
Gnarlhound.targetChance(10)
Gnarlhound.type("blood")
Gnarlhound.health(198)
Gnarlhound.experience(60)
Gnarlhound.speed(200) # incorrect
Gnarlhound.walkAround(1,1,1) # energy, fire, poison
Gnarlhound.behavior(summonable=465, hostile=True, illusionable=True, convinceable=465, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=20)
Gnarlhound.immunity(0,0,0) # paralyze, invisible, lifedrain
Gnarlhound.defense(12, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Gnarlhound.loot( ("meat", 38.75, 3), (3976, 98.5, 3), ("shaggy tail", 20.5) )
Gnarlhound.melee(70)