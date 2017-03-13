Hunter = genMonster("Hunter", 129, 6080)
Hunter.outfit(95, 116, 121, 115)
Hunter.targetChance(10)
Hunter.type("blood")
Hunter.health(150)
Hunter.experience(150)
Hunter.speed(210) # Correct
Hunter.walkAround(1,1,1) # energy, fire, poison
Hunter.behavior(summonable=0, hostile=True, illusionable=True, convinceable=530, pushable=False, pushItems=True, pushCreatures=False, targetDistance=4, runOnHealth=15)
Hunter.voices("Guess who we are hunting!", "Guess who we're hunting, hahaha!", "Bullseye!", "You'll make a nice trophy!")
Hunter.immunity(0,0,0) # paralyze, invisible, lifedrain
Hunter.defense(9, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=0.8, death=1.0, physical=1.05, drown=1.0)
Hunter.melee(20)
Hunter.distance(100, ANIMATION_ARROW, chance(21))
Hunter.loot( ("arrow", 100, 22), ("orange", 29.75, 2), ("torch", 2.75), ("dragon necklace", 2.75), (12425, 10.0), ("bow", 6.0), ("brass armor", 5.25), ("deer trophy", 0.5), ("roll", 17.0, 2), ("brass helmet", 4.75), ("poison arrow", 12.25, 4), ("burst arrow", 10.5, 3), ("wolf trophy", 0.5), ("small ruby", 0.25), ("sniper gloves", 0.25), ("slingshot", 0.25) )