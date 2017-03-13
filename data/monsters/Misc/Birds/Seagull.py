Seagull = genMonster("Seagull", 223, 6076)
Seagull.targetChance(0)
Seagull.type("blood")
Seagull.health(25)
Seagull.experience(0)
Seagull.speed(200) #incorrect
Seagull.walkAround(1,1,1) # energy, fire, poison
Seagull.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=25)
Seagull.immunity(0,0,0) # paralyze, invisible, lifedrain
Seagull.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Seagull.melee(3)#summons only? probably incorrect information