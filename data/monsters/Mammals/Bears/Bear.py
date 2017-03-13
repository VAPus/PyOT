bear = genMonster("Bear", 16, 5975)
bear.type("blood")
bear.health(80)
bear.experience(23)
bear.targetChance(10)
bear.speed(156) # speed correct
bear.walkAround(1,1,1) # energy, fire, poison
bear.behavior(summonable=300, hostile=True, illusionable=True, convinceable=300, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=15)
bear.voices("Grrrr", "Groar")
bear.immunity(0,0,0) # paralyze, invisible, lifedrain
bear.defense(7, fire=1.0, earth=1.0, energy=1.0, ice=1.1, holy=0.9, death=1.5, physical=1.0, drown=1.0)
bear.loot( ("meat", 38.75, 4), ("ham", 19.75, 2), ("bear paw", 2.0), ("honeycomb", 0.75) )
bear.melee(25)