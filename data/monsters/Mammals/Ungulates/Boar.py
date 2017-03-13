# bad
boar = genMonster("Boar", 380, 13308)
boar.type("blood")
boar.health(198)
boar.experience(60)
boar.targetChance(10)
boar.speed(200) #incorrect
boar.walkAround(1,1,1) # energy, fire, poison
boar.behavior(summonable=465, hostile=True, illusionable=True, convinceable=465, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=20)
boar.voices("Grunt Grunt, Grunt")
boar.immunity(0,0,0) # paralyze, invisible, lifedrain
boar.defense(3, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
boar.loot( ("haunch of boar", 31.25, 2), (2148, 100, 20) ),
boar.melee(50)#or more