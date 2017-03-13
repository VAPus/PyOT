blood_crab = genMonster("Blood Crab", 200, 6075)
blood_crab.type("blood")
blood_crab.health(320)
blood_crab.experience(180)
blood_crab.targetChance(10)
blood_crab.speed(200) # speed incorrect
blood_crab.walkAround(1,1,0) # energy, fire, poison
blood_crab.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
blood_crab.immunity(0,0,0) # paralyze, invisible, lifedrain
blood_crab.defense(31, fire=0, earth=0, energy=1.05, ice=0, holy=1.0, death=1.0, physical=0.99, drown=0)

blood_crab.melee(111)