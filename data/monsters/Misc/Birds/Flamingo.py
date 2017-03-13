Flamingo = genMonster("Flamingo", 212, 6054)
Flamingo.targetChance(10)
Flamingo.type("blood")
Flamingo.health(25)
Flamingo.experience(0)
Flamingo.speed(160) # correct
Flamingo.walkAround(1,1,1) # energy, fire, poison
Flamingo.behavior(summonable=250, hostile=False, illusionable=True, convinceable=250, pushable=True, pushItems=False, pushCreatures=False, targetDistance=0, runOnHealth=0)
Flamingo.immunity(0,0,0) # paralyze, invisible, lifedrain
Flamingo.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Flamingo.loot( ("downy feather", 0.5) )