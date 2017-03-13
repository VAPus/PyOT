Gazer = genMonster("Gazer", 226, 6079)
Gazer.targetChance(10)
Gazer.type("blood")
Gazer.health(120)
Gazer.experience(90)
Gazer.speed(200) # not correct
Gazer.walkAround(1,1,0) # energy, fire, poison
Gazer.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=4, runOnHealth=0)
Gazer.voices("Mommy!?", "Buuuuhaaaahhaaaaa!", "We need mana!")
Gazer.immunity(0,1,0) # paralyze, invisible, lifedrain
Gazer.defense(4, fire=0.4, earth=0, energy=0.9, ice=0.8, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Gazer.melee(20)#ish~