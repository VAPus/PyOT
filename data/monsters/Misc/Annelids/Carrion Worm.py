Carrion_Worm = genMonster("Carrion Worm", 192, 6069)
Carrion_Worm.targetChance(0)
Carrion_Worm.type("blood")
Carrion_Worm.health(145)
Carrion_Worm.experience(70)
Carrion_Worm.speed(130) # Correct
Carrion_Worm.walkAround(1,1,1) # energy, fire, poison
Carrion_Worm.behavior(summonable=0, hostile=True, illusionable=False, convinceable=380, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Carrion_Worm.immunity(0,0,0) # paralyze, invisible, lifedrain
Carrion_Worm.defense(9, fire=1.05, earth=0.8, energy=0.9, ice=1.05, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Carrion_Worm.melee(45)
Carrion_Worm.loot( ("meat", 14.0, 2), (2148, 100, 26), ("carrion worm fang", 11.0), (3976, 8.25, 2) )