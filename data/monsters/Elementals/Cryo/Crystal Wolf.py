# Bad fixed
crystal_wolf = genMonster("Crystal Wolf", 226, 6079) # unkown yet
crystal_wolf.targetChance(10)
crystal_wolf.type("blood")
crystal_wolf.health(750)
crystal_wolf.experience(275)
crystal_wolf.speed(200) #incorrect
crystal_wolf.walkAround(1,1,1) # energy, fire, poison
crystal_wolf.behavior(summonable=0, hostile=True, illusionable=True, convinceable=305, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
crystal_wolf.voices("Raaaarrr!")
crystal_wolf.immunity(0,0,0) # paralyze, invisible, lifedrain
crystal_wolf.defense(30, fire=1.1, earth=1.0, energy=1.0, ice=0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
crystal_wolf.melee(80)#no idea