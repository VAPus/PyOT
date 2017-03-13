Terror_Bird = genMonster("Terror Bird", 218, 6057)
Terror_Bird.targetChance(10)
Terror_Bird.type("blood")
Terror_Bird.health(300)
Terror_Bird.experience(150)
Terror_Bird.speed(212)
Terror_Bird.walkAround(1,1,1) # energy, fire, poison
Terror_Bird.behavior(summonable=490, hostile=True, illusionable=True, convinceable=490, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Terror_Bird.voices("Carrah! Carrah!", "Gruuuh Gruuuh.", "CRAAAHHH!")
Terror_Bird.immunity(0,0,0) # paralyze, invisible, lifedrain
Terror_Bird.defense(18, fire=1.1, earth=1.1, energy=0.8, ice=0.8, holy=1.0, death=1.05, physical=1.0, drown=1.0)
Terror_Bird.loot( (2148, 100, 30), ("meat", 48.75, 3), ("terrorbird beak", 11.5), ("colourful feather", 3.0), (3976, 9.0), ("health potion", 1.25), ("seeds", 0.25) )
Terror_Bird.melee(90)