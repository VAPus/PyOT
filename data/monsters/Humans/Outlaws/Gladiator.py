Gladiator = genMonster("Gladiator", 131, 6080)
Gladiator.outfit(78, 3, 79, 114)
Gladiator.targetChance(10)
Gladiator.type("blood")
Gladiator.health(185)
Gladiator.experience(90)
Gladiator.speed(200)
Gladiator.walkAround(1,1,1) # energy, fire, poison
Gladiator.behavior(summonable=0, hostile=True, illusionable=False, convinceable=470, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=18)
Gladiator.voices("You are no match for me!", "Feel my prowess.", "Take this!")
Gladiator.immunity(0,0,0) # paralyze, invisible, lifedrain
Gladiator.defense(15, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=0.9, death=1.05, physical=0.95, drown=1.0)
Gladiator.melee(90)
Gladiator.loot( ("plate shield", 9.25), ("mace", 10.75), ("chain helmet", 4.75), (2148, 100, 28), ("sword", 10.75), ("meat", 20.5), ("brass armor", 1.75), ("steel shield", 0.75), ("iron helmet", 0.25), ("belted cape", 0.5) )