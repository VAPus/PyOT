Azure_Frog = genMonster("Azure Frog", 226, 6079)
Azure_Frog.outfit(69, 66, 69, 66)
Azure_Frog.type("blood")
Azure_Frog.health(60)
Azure_Frog.experience(20)
Azure_Frog.targetChance(10)
Azure_Frog.speed(200) # speed incorrect
Azure_Frog.walkAround(1,1,1) # energy, fire, poison
Azure_Frog.behavior(summonable=0, hostile=True, illusionable=False, convinceable=305, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Azure_Frog.voices("Ribbit!", "Ribbit! Ribbit!")
Azure_Frog.immunity(0,0,0) # paralyze, invisible, lifedrain
Azure_Frog.defense(9, fire=1.1, earth=1, energy=1, ice=0.85, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Azure_Frog.loot( (2148, 100, 10), (3976, 8.75) )

Azure_Frog.melee(24)
