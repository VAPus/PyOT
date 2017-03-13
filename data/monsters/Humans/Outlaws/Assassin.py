Assassin = genMonster("Assassin", 152, 6080)
Assassin.outfit(95, 95, 95, 95)
Assassin.addons(3)
Assassin.targetChance(10)
Assassin.type("blood")
Assassin.health(175)
Assassin.experience(105)
Assassin.speed(224) # correct
Assassin.walkAround(1,1,1) # energy, fire, poison
Assassin.behavior(summonable=0, hostile=True, illusionable=True, convinceable=450, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
Assassin.voices("You are on my deathlist!", "Die!", "Feel the hand of death!")
Assassin.immunity(0,1,0) # paralyze, invisible, lifedrain
Assassin.defense(22, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.25, drown=1.0)
Assassin.melee(120)
Assassin.distance(40, ANIMATION_THROWINGSTAR, chance(21))
Assassin.loot( ("throwing star", 50.5, 14), (2148, 100, 50), ("knife", 10.25), ("torch", 42.25, 2), ("viper star", 18.0, 7), ("combat knife", 4.0), ("steel shield", 1.25), ("steel helmet", 2.75), ("plate shield", 2.0), ("battle shield", 1.5), ("leopard armor", 0.5), ("horseman helmet", 0.25), ("small diamond", 0.0025) )