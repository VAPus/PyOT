dragonling = genMonster("Dragonling", 505, 18441) #mostly unknown
dragonling.health(2600, healthmax=2600)
dragonling.type("blood")
dragonling.defense(armor=20, fire=0, earth=1.02, energy=0.98, ice=0.98, holy=1, death=1, physical=1.02, drown=1)
dragonling.experience(2200)
dragonling.speed(300) #unknown
dragonling.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
dragonling.walkAround(energy=1, fire=0, poison=0)
dragonling.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
dragonling.voices("FI?", "FCHHHHHHHHHHHHHHHH")
dragonling.melee(200)