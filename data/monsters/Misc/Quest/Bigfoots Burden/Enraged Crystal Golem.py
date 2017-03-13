enraged_crystal_golem = genMonster("Enraged Crystal Golem", 508, 18466)  #mostly unkniown including blood
enraged_crystal_golem.health(700, healthmax=700)
enraged_crystal_golem.type("blood")
enraged_crystal_golem.defense(armor=30, fire=0, earth=1, energy=1, ice=0, holy=1, death=1, physical=0.85, drown=1)
enraged_crystal_golem.experience(550)
enraged_crystal_golem.speed(350) #unknown
enraged_crystal_golem.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
enraged_crystal_golem.walkAround(energy=0, fire=0, poison=0)
enraged_crystal_golem.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
enraged_crystal_golem.voices("Crrrrk! Chhhhr!")
enraged_crystal_golem.melee(150)