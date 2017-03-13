ghoulish_hyaena = genMonster("Ghoulish Hyaena", 94, 6026)
ghoulish_hyaena.health(400)
ghoulish_hyaena.type("blood")
ghoulish_hyaena.defense(armor=22, fire=1, earth=0.3, energy=1, ice=1, holy=1, death=0, physical=1, drown=1)
ghoulish_hyaena.experience(195)
ghoulish_hyaena.speed(240)#unknown speed
ghoulish_hyaena.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=30)
ghoulish_hyaena.walkAround(energy=0, fire=0, poison=0)
ghoulish_hyaena.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
ghoulish_hyaena.voices("Grawrrr!!", "Hoouu!")
ghoulish_hyaena.melee(170)#incorrect
ghoulish_hyaena.loot( (2148, 100, 40), ("health potion", 19.0), ("meat", 47.75), (3976, 100, 7), ("small ruby", 5.75, 2) )