Elephant = genMonster("Elephant", 211, 6052)
Elephant.targetChance(10)
Elephant.type("blood")
Elephant.health(320)
Elephant.experience(160)
Elephant.speed(190) # correct
Elephant.walkAround(1,1,1) # energy, fire, poison
Elephant.behavior(summonable=500, hostile=True, illusionable=True, convinceable=500, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Elephant.voices("Hooooot-Toooooot!", "Tooooot!", "Troooooot!")
Elephant.immunity(0,0,0) # paralyze, invisible, lifedrain
Elephant.defense(22, fire=1.0, earth=1.0, energy=1.1, ice=0.8, holy=1.0, death=1.0, physical=0.9, drown=1.0)
Elephant.loot( ("meat", 42.25, 4), ("ham", 29.25, 3), (8614, 1.5, 2), ("tusk shield", 0.0025) )
Elephant.melee(100)