Black_Knight = genMonster("Black Knight", 131, 6080)
Black_Knight.outfit(95, 95, 95, 95)
Black_Knight.addons(3)
Black_Knight.targetChance(10)
Black_Knight.type("blood")
Black_Knight.health(1800)
Black_Knight.experience(1600)
Black_Knight.speed(200) # Incorrect
Black_Knight.walkAround(0,0,0) # energy, fire, poison
Black_Knight.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Black_Knight.voices("No prisoners!", "By Bolg's blood", "You're no match for me!", "NO MERCY!", "MINE!")
Black_Knight.immunity(1,1,1) # paralyze, invisible, lifedrain
Black_Knight.defense(100, fire=0.05, earth=0, energy=0.2, ice=0, holy=1.1, death=0.8, physical=0.8, drown=1.0)
Black_Knight.melee(300)
Black_Knight.distance(200, ANIMATION_SPEAR, chance(21))
Black_Knight.loot( ("spear", 60.5, 3), ("steel helmet", 12.25), (2148, 100, 128), ("two handed sword", 10.0), ("warrior helmet", 4.75), ("halberd", 12.25), ("dark helmet", 3.0), ("battle hammer", 6.5), ("knight axe", 3.0), ("lightning legs", 0.75), ("dark armor", 1.75), ("brown bread", 28.75, 2), ("brass legs", 13.75), ("rope", 14.25), ("plate armor", 11.25), ("dragon lance", 1.0), ("knight legs", 1.75), ("knight armor", 0.5), ("ruby necklace", 1.0), ("boots of haste", 0.25) )