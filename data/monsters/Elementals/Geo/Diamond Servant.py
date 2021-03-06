diamond_servant = genMonster("Diamond Servant", 397, 5980)
diamond_servant.health(1000)
diamond_servant.type("blood")
diamond_servant.defense(armor=26, fire=0.9, earth=0.25, energy=0, ice=1, holy=1.15, death=1, physical=1, drown=1)
diamond_servant.experience(700)
diamond_servant.speed(250)
diamond_servant.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
diamond_servant.walkAround(energy=0, fire=1, poison=0)
diamond_servant.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
diamond_servant.voices("Error. LOAD 'PROGRAM',8,1", "Remain. Obedient.")
diamond_servant.melee(100)
diamond_servant.loot( (2148, 100, 168), ("soul orb", 44.75), ("strong health potion", 6.75), ("life crystal", 11.5), ("gear wheel", 6.75), ("crystal pedestal", 2.75), ("slime mould", 1.0), ("gear crystal", 5.75), ("strong mana potion", 6.75), ("lightning pendant", 2.75), ("mastermind potion", 1.0), ("might ring", 1.0) )