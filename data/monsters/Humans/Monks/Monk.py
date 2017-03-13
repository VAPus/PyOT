Monk = genMonster("Monk", 57, 6080)
Monk.targetChance(10)
Monk.type("blood")
Monk.health(240)
Monk.experience(200)
Monk.speed(240) # Correct
Monk.walkAround(1,1,1) # energy, fire, poison
Monk.behavior(summonable=600, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Monk.voices("Repent Heretic!", "A prayer to the almighty one!", "I will punish the sinners!")
Monk.immunity(0,1,0) # paralyze, invisible, lifedrain
Monk.defense(27, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=0.5, death=0.5, physical=1.05, drown=1.0)
Monk.melee(120)
Monk.loot( ("rope belt", 3.25), ("bread", 18.75), ("book of prayers", 5.5), (2148, 100, 18), ("lamp", 1.25), ("ankh", 2.25), ("staff", 0.25), ("scroll", 2.25), ("brown flask", 1.0), ("safety pin", 1.0), ("life crystal", 0.75), ("power ring", 0.0025), ("sandals", 0.75) )