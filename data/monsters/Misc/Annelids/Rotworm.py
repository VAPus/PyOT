Rotworm = genMonster("Rotworm", 26, 5967)
Rotworm.targetChance(0)
Rotworm.type("blood")
Rotworm.health(65)
Rotworm.experience(40)
Rotworm.speed(116)
Rotworm.walkAround(1,1,1) # energy, fire, poison
Rotworm.behavior(summonable=0, hostile=True, illusionable=False, convinceable=305, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Rotworm.immunity(0,0,0) # paralyze, invisible, lifedrain
Rotworm.defense(9, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Rotworm.melee(40)
Rotworm.loot( ("lump of dirt", 10.0), ("meat", 20.0, 2), (2148, 100, 17), ("ham", 19.75, 2), (3976, 5.75, 3), ("sword", 3.0), ("mace", 4.25) )