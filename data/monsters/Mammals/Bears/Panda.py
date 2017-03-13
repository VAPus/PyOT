Panda = genMonster("Panda", 123, 6049)
Panda.targetChance(10)
Panda.type("blood")
Panda.health(80)
Panda.experience(23)
Panda.speed(200) #incorrect
Panda.walkAround(1,1,0) # energy, fire, poison
Panda.behavior(summonable=300, hostile=True, illusionable=True, convinceable=300, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=10)
Panda.voices("Groar", "Grrrrr")
Panda.immunity(0,0,0) # paralyze, invisible, lifedrain
Panda.defense(9, fire=1.1, earth=0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Panda.loot( ("ham", 34.0, 2), ("meat", 72.25, 4), ("bamboo stick", 3.0) )
Panda.melee(16)