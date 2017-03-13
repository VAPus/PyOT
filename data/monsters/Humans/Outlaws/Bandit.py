Bandit = genMonster("Bandit", 129, 6080)
Bandit.outfit(58, 59, 45, 114)
Bandit.targetChance(10)
Bandit.type("blood")
Bandit.health(245)
Bandit.experience(65)
Bandit.speed(180) # Correct
Bandit.walkAround(1,1,1) # energy, fire, poison
Bandit.behavior(summonable=450, hostile=True, illusionable=True, convinceable=450, pushable=True, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=25)
Bandit.voices("Hand me your purse!", "Your money or your life!")
Bandit.immunity(0,0,0) # paralyze, invisible, lifedrain
Bandit.defense(11, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.1, drown=1.0)
Bandit.melee(43)
Bandit.loot( (2148, 100, 27), ("axe", 31.75), ("brass shield", 18.0), ("mace", 10.75), ("chain helmet", 5.5), ("leather legs", 14.0), ("brass armor", 2.25), ("tomato", 10.5, 2), ("iron helmet", 0.5) )