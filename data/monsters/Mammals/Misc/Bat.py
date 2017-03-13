bat = genMonster("Bat", 122, 6053)
bat.type("blood")
bat.health(30)
bat.experience(10)
bat.targetChance(10)
bat.speed(200) # speed correct
bat.walkAround(1,1,1) # energy, fire, poison
bat.behavior(summonable=250, hostile=True, illusionable=True, convinceable=205, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=3)
bat.voices("Flap! Flap!")
bat.immunity(0,0,0) # paralyze, invisible, lifedrain
bat.defense(2, fire=1.0, earth=1.05, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
bat.loot( ("bat wing", 1.0, 3) )
bat.melee(8)