Stampor = genMonster("Stampor", 381, 13315)
Stampor.targetChance(10)
Stampor.type("blood")
Stampor.health(1200)
Stampor.experience(780)
Stampor.speed(200) #incorrect
Stampor.walkAround(1,1,1) # energy, fire, poison
Stampor.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Stampor.voices("KRRRRRNG")
Stampor.immunity(1,1,0) # paralyze, invisible, lifedrain
Stampor.defense(20, fire=0.8, earth=1.0, energy=0.8, ice=0.9, holy=0.5, death=0.9, physical=1.0, drown=1.0) # not full correct
Stampor.loot( ("spiked squelcher", 0.25), ("knight armor", 1.0), ("war hammer", 1.0), ("hollow stampor hoof", 2.75), ("stampor horn", 5.25), ("strong health potion", 7.0, 2), ("platinum coin", 15.0, 2), ("strong mana potion", 7.5, 2), ("small topaz", 12.0, 2), ("stampor talons", 10.75), (2148, 100, 244) ) # , ('stampor talon', 11), ('stampor horn', 5.5), ('hollow stampor hoof', 3.5)
Stampor.melee(130)