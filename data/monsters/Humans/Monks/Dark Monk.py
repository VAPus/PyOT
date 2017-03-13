Dark_Monk = genMonster("Dark Monk", 225, 6080)
Dark_Monk.targetChance(10)
Dark_Monk.type("blood")
Dark_Monk.health(190)
Dark_Monk.experience(145)
Dark_Monk.speed(230) # Correct
Dark_Monk.walkAround(1,1,1) # energy, fire, poison
Dark_Monk.behavior(summonable=0, hostile=True, illusionable=True, convinceable=480, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Dark_Monk.voices("You are no match to us!", "Your end has come!", "This is where your path will end!")
Dark_Monk.immunity(0,1,0) # paralyze, invisible, lifedrain
Dark_Monk.defense(22, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=0.9, death=0.6, physical=1.05, drown=1.0)
Dark_Monk.melee(100)
Dark_Monk.loot( ("dark rosary", 11.25), ("sandals", 0.75), (2148, 100, 18), ("mana potion", 1.0), ("safety pin", 1.0), ("lamp", 0.25), ("rope belt", 7.25), ("bread", 22.5), ("life crystal", 1.25), ("book of prayers", 2.25), ("ankh", 1.25), ("scroll", 2.25), ("brown flask", 0.25), ("power ring", 0.0025) )