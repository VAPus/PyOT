Polar_Bear = genMonster("Polar Bear", 42, 5987)
Polar_Bear.targetChance(10)
Polar_Bear.type("blood")
Polar_Bear.health(85)
Polar_Bear.experience(28)
Polar_Bear.speed(156) #correct
Polar_Bear.walkAround(1,1,1) # energy, fire, poison
Polar_Bear.behavior(summonable=315, hostile=True, illusionable=True, convinceable=315, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=5)
Polar_Bear.voices("GROARRR!")
Polar_Bear.immunity(0,0,0) # paralyze, invisible, lifedrain
Polar_Bear.defense(7, fire=0.9, earth=1.0, energy=1.05, ice=0.8, holy=1.0, death=1.1, physical=1.0, drown=1.0)
Polar_Bear.loot( ("ham", 51.0, 2), ("meat", 50.25, 4), ("polar bear paw", 0.75) ) #only drops polar bear paw
Polar_Bear.melee(30)
