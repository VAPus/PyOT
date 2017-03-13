Rift_Worm = genMonster("Rift Worm", 295, 0)
Rift_Worm.targetChance(10)
Rift_Worm.type("blood")
Rift_Worm.health(2800)
Rift_Worm.experience(1950)
Rift_Worm.speed(136) # Correct
Rift_Worm.walkAround(1,1,1) # energy, fire, poison
Rift_Worm.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Rift_Worm.immunity(1,1,1) # paralyze, invisible, lifedrain
Rift_Worm.defense(31, fire=1.05, earth=0.7, energy=0.9, ice=1.05, holy=1.05, death=0.95, physical=1.05, drown=1.0)
Rift_Worm.melee(160)#ish?