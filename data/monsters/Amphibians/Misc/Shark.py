shark = genMonster("Shark", 8, 5980)
shark.health(1200, healthmax=1200)
shark.type("blood")
shark.defense(armor=15, fire=1, earth=0.8, energy=1.05, ice=1, holy=1, death=1, physical=1, drown=0)
shark.experience(700)
shark.speed(300) #incorrect
shark.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
shark.walkAround(energy=1, fire=0, poison=0)
shark.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
shark.voices("Rarr chomp chomp!")
shark.melee(10) #?