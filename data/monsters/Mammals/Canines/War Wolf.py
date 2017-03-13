War_Wolf = genMonster("War Wolf", 3, 6009)
War_Wolf.targetChance(10)
War_Wolf.type("blood")
War_Wolf.health(140)
War_Wolf.experience(55)
War_Wolf.speed(264) #correct
War_Wolf.walkAround(1,1,1) # energy, fire, poison
War_Wolf.behavior(summonable=0, hostile=True, illusionable=True, convinceable=420, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
War_Wolf.voices("Yoooohhuuuu!", "Grrrrrrrr")
War_Wolf.immunity(0,0,0) # paralyze, invisible, lifedrain
War_Wolf.defense(9, fire=1.0, earth=0.8, energy=1.0, ice=1.1, holy=0.9, death=1.08, physical=10, drown=1.0)
War_Wolf.loot( ("ham", 22.5), ("wolf paw", 0.75, 3), ("warwolf fur", 3.0) ) # 1884 is a wolf trophy 
War_Wolf.melee(50)