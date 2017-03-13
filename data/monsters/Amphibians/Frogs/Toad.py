Toad = genMonster("Toad", 222, 6077)
Toad.targetChance(10)
Toad.type("blood")
Toad.health(135)
Toad.experience(60)
Toad.speed(210) #correct
Toad.walkAround(1,1,1) # energy, fire, poison
Toad.behavior(summonable=400, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=10)
Toad.voices("Ribbit!", "Ribbit! Ribbit!")
Toad.immunity(0,0,0) # paralyze, invisible, lifedrain
Toad.defense(7, fire=1.1, earth=0.8, energy=1.0, ice=0.8, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Toad.loot( (2148, 100, 20), ("poisonous slime", 4.25), ("fish", 20.0), ("war hammer", 0.25), ("mace", 3.0) )

Toad.melee(30, condition=CountdownCondition(CONDITION_POISON, 1), conditionChance=100)
Toad.selfSpell("Haste", 360, 360, length=5, check=chance(21)) #?
Toad.targetSpell(2292, 8, 17, check=chance(21)) #is the range 1?
