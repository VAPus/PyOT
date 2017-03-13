Wolf = genMonster("Wolf", 27)
Wolf.targetChance(0)
Wolf.type("blood")
Wolf.health(25)
Wolf.experience(18)
Wolf.speed(164) #correct
Wolf.walkAround(1,1,1) # energy, fire, poison
Wolf.behavior(summonable=255, hostile=True, illusionable=True, convinceable=255, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=8)
Wolf.voices("Yooooohhuuuu!", "Grrrrrrrr")
Wolf.immunity(0,0,0) # paralyze, invisible, lifedrain
Wolf.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.1, holy=0.9, death=1.05, physical=1.0, drown=1.0)
Wolf.loot( ("meat", 67.5, 2), ("wolf paw", 1.0) )
Wolf.melee(19)
