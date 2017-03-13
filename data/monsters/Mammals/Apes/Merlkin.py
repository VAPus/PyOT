Merlkin = genMonster("Merlkin", 117, 6044)
Merlkin.targetChance(10)
Merlkin.type("blood")
Merlkin.health(235)
Merlkin.experience(145)
Merlkin.speed(194)
Merlkin.walkAround(1,1,1) # energy, fire, poison
Merlkin.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=4, runOnHealth=0)
Merlkin.voices("Ugh! Ugh! Ugh!", "Holy banana!", "Chakka! Chakka!")
Merlkin.immunity(0,1,0) # paralyze, invisible, lifedrain
Merlkin.defense(18, fire=0.8, earth=1.0, energy=0.9, ice=1.15, holy=0.9, death=1.05, physical=1.0, drown=1.0)
Merlkin.melee(30)
Merlkin.loot( (2148, 100, 44), ("banana staff", 0.25), ("banana", 46.75, 11), ("wand of decay", 1.0), (2162, 3.0), ("banana sash", 2.0), ("orange", 3.0, 5), ("mana potion", 0.75), ("small amethyst", 0.25), ("ape fur", 0.75, 3) )