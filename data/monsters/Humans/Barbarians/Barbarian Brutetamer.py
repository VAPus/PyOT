Barbarian_Brutetamer = genMonster("Barbarian Brutetamer", 264, 6081)
Barbarian_Brutetamer.outfit(78,116,95,121)
Barbarian_Brutetamer.targetChance(10)
Barbarian_Brutetamer.type("blood")
Barbarian_Brutetamer.health(145)
Barbarian_Brutetamer.experience(90)
Barbarian_Brutetamer.speed(178) #correct
Barbarian_Brutetamer.walkAround(1,1,1) # energy, fire, poison
Barbarian_Brutetamer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=4, runOnHealth=14)
Barbarian_Brutetamer.voices("To me, creatures of the wold!", "My instincts tell me about your cowardice.", "Feel the power of the beast!")
Barbarian_Brutetamer.immunity(1,1,1) # paralyze, invisible, lifedrain
Barbarian_Brutetamer.defense(9, fire=1.0, earth=0.8, energy=1.0, ice=0.5, holy=0.9, death=1.05, physical=1.1, drown=1.0)
Barbarian_Brutetamer.summon("War Wolf", 10)
Barbarian_Brutetamer.maxSummons(2)
Barbarian_Brutetamer.melee(20)
Barbarian_Brutetamer.loot( ("ham", 7.25, 3), (2148, 100, 15), ("hunting spear", 4.75), ("fur bag", 8.25), ("corncob", 16.25, 2), ("staff", 6.5), ("chain armor", 9.5), ("mana potion", 0.75), ("book", 4.25), ("fur boots", 0.0025), ("brutetamer's staff", 0.25), ("mammoth fur shorts", 0.0025), ("mammoth fur cape", 0.0025) )