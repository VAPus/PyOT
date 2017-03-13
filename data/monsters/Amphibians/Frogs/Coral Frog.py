coral_frog = genMonster("Coral Frog", 226, 6079)
coral_frog.outfit(69, 66, 69, 66)
coral_frog.targetChance(10)
coral_frog.type("blood")
coral_frog.health(60)
coral_frog.experience(20)
coral_frog.speed(200) #incorrect
coral_frog.walkAround(1,1,1) # energy, fire, poison
coral_frog.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
coral_frog.voices("Ribbit!", "Ribbit! Ribbit!")
coral_frog.immunity(0,0,0) # paralyze, invisible, lifedrain
coral_frog.defense(9, fire=1.1, earth=1.0, energy=1.0, ice=0.85, holy=1.0, death=1.0, physical=1.0, drown=1.0)
coral_frog.loot( (2148, 100, 10), (3976, 13.75) )

coral_frog.melee(24)
