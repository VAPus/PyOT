# bad  (suppose to summon enraged or hurt white deer when it dies)
White_Deer = genMonster("White Deer", 400, 6079) # uknown yet
White_Deer.targetChance(10)
White_Deer.type("blood")
White_Deer.health(195)
White_Deer.experience(0)
White_Deer.speed(220)
White_Deer.walkAround(1,1,1) # energy, fire, poison
White_Deer.behavior(summonable=0, hostile=False, illusionable=True, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=195)
White_Deer.voices("wheeze", "ROOOAAARR!!", "sniff", "bell")
White_Deer.immunity(0,0,0) # paralyze, invisible, lifedrain
White_Deer.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)