cat = genMonster("Cat", 276, 7637)
cat.type("blood")
cat.health(20)
cat.experience(0)
cat.targetChance(10)
cat.speed(124) #?
cat.walkAround(1,1,1) # energy, fire, poison
cat.behavior(summonable=220, hostile=True, illusionable=True, convinceable=220, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
cat.voices("Mew!", "Meow!", "Meow meow!")
cat.immunity(0,0,0) # paralyze, invisible, lifedrain
cat.defense(2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)