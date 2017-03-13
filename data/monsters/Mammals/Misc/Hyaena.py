Hyaena = genMonster("Hyaena", 94, 6026)
Hyaena.targetChance(10)
Hyaena.type("blood")
Hyaena.health(60)
Hyaena.experience(20)
Hyaena.speed(196) #correct
Hyaena.walkAround(1,1,1) # energy, fire, poison
Hyaena.behavior(summonable=275, hostile=True, illusionable=True, convinceable=275, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=30)
Hyaena.voices("Grrrrrr", "Hou hou hou!")
Hyaena.immunity(0,0,0) # paralyze, invisible, lifedrain
Hyaena.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Hyaena.loot( (3976, 100, 3), ("meat", 39.25, 2) )
Hyaena.melee(20)