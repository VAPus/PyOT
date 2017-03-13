Orchid_Frog = genMonster("Orchid Frog", 226, 6079)
Orchid_Frog.outfit(109, 14, 109, 114)
Orchid_Frog.targetChance(10)
Orchid_Frog.type("blood")
Orchid_Frog.health(60)
Orchid_Frog.experience(20)
Orchid_Frog.speed(200) # incorrect
Orchid_Frog.walkAround(1,1,1) # energy, fire, poison
Orchid_Frog.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Orchid_Frog.voices("Ribbit!", "Ribbit! Ribbit!")
Orchid_Frog.immunity(0,0,0) # paralyze, invisible, lifedrain
Orchid_Frog.defense(9, fire=1.1, earth=1.0, energy=1.0, ice=0.85, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Orchid_Frog.loot( (2148, 100, 10), (3976, 11.75) )

Orchid_Frog.melee(24)
