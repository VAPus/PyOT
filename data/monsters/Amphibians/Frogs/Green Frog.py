Green_Frog = genMonster("Green Frog", 224, 6079)
Green_Frog.outfit(69, 66, 69, 66)
Green_Frog.targetChance(10)
Green_Frog.type("slime")
Green_Frog.health(25)
Green_Frog.experience(0)
Green_Frog.speed(200) #incorrect
Green_Frog.walkAround(1,1,1) # energy, fire, poison
Green_Frog.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=False, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=25)
Green_Frog.voices("Ribbit!", "Ribbit! Ribbit!")
Green_Frog.immunity(0,0,0) # paralyze, invisible, lifedrain
Green_Frog.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
