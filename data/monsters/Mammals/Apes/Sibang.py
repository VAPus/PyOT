Sibang = genMonster("Sibang", 118, 6045)
Sibang.targetChance(10)
Sibang.type("blood")
Sibang.health(225)
Sibang.experience(105)
Sibang.speed(214) # correct
Sibang.walkAround(1,1,1) # energy, fire, poison
Sibang.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=4, runOnHealth=0)
Sibang.voices("Eeeeek! Eeeeek!", "Huh! Huh! Huh!", "Ahhuuaaa!")
Sibang.immunity(0,1,0) # paralyze, invisible, lifedrain
Sibang.defense(11, fire=0.75, earth=1.0, energy=1.0, ice=1.15, holy=0.9, death=1.05, physical=1.0, drown=1.0)
Sibang.melee(40)
Sibang.distance(55, ANIMATION_SMALLSTONE, chance(21))
Sibang.loot( ("orange", 61.5, 5), ("small stone", 61.5, 3), ("banana sash", 5.0), (2148, 100, 35), ("banana", 48.0, 11), ("ape fur", 1.25, 3), ("coconut", 3.75, 3), ("melon", 1.0) )