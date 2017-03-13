Amazon = genMonster("Amazon", 137, 6081)
Amazon.outfit(113, 120, 114, 132)
Amazon.targetChance(10)
Amazon.type("blood")
Amazon.health(110)
Amazon.experience(60)
Amazon.speed(172) # correct
Amazon.walkAround(1,1,1) # energy, fire, poison
Amazon.behavior(summonable=390, hostile=True, illusionable=True, convinceable=390, pushable=True, pushItems=True, pushCreatures=False, targetDistance=4, runOnHealth=10)
Amazon.voices("Your head shall be mine!", "Your head will be mine!", "Yeee ha!")
Amazon.immunity(0,0,0) # paralyze, invisible, lifedrain
Amazon.defense(11, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.05, drown=1.0)
Amazon.melee(45)
Amazon.distance(40, ANIMATION_THROWINGKNIFE, chance(21))
Amazon.loot( ("sabre", 24.25), ("brown bread", 32.0), ("dagger", 81.5), ("protective charm", 5.0), ("skull", 100, 2), (2148, 100, 20), ("girlish hair decoration", 11.5), ("torch", 2.0), ("crystal necklace", 0.25) )