jellyfish = genMonster("Jellyfish", 452, 15284)
jellyfish.health(55)
jellyfish.type("blood")
jellyfish.defense(armor=5, fire=0, earth=0, energy=1.05, ice=1, holy=1, death=1, physical=1.05, drown=0)
jellyfish.experience(0)
jellyfish.speed(250) #?
jellyfish.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
jellyfish.walkAround(energy=1, fire=0, poison=0)
jellyfish.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
jellyfish.voices("Luuurrrp!")
jellyfish.melee(5) #?