Thornback_Tortoise = genMonster("Thornback Tortoise", 198, 6073)
Thornback_Tortoise.targetChance(10)
Thornback_Tortoise.type("blood")
Thornback_Tortoise.health(300)
Thornback_Tortoise.experience(150)
Thornback_Tortoise.speed(200) #incorrect
Thornback_Tortoise.walkAround(1,1,1) # energy, fire, poison
Thornback_Tortoise.behavior(summonable=0, hostile=True, illusionable=True, convinceable=490, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Thornback_Tortoise.immunity(0,0,0) # paralyze, invisible, lifedrain
Thornback_Tortoise.defense(29, fire=1.1, earth=0.8, energy=1.0, ice=0.8, holy=1.0, death=1.0, physical=0.7, drown=1.0)
Thornback_Tortoise.loot( (2148, 100, 30), ("fish", 10.0), ("thorn", 5.25), ("white mushroom", 1.5), ("tortoise egg", 2.0, 3), ("health potion", 0.75), ("war hammer", 0.5), ("brown mushroom", 0.75) )
Thornback_Tortoise.melee(110)
#Envenom 2 hp/turn.