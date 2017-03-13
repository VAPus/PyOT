Valkyrie = genMonster("Valkyrie", 139, 6080)
Valkyrie.outfit(113, 57, 95, 113)
Valkyrie.targetChance(10)
Valkyrie.type("blood")
Valkyrie.health(190)
Valkyrie.experience(85)
Valkyrie.speed(176) # Correct
Valkyrie.walkAround(1,1,1) # energy, fire, poison
Valkyrie.behavior(summonable=450, hostile=True, illusionable=True, convinceable=450, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=10)
Valkyrie.voices("Another head for me!", "Head off!", "Your hea will be mine!", "Stand still!", "One more head for me!")
Valkyrie.immunity(0,0,0) # paralyze, invisible, lifedrain
Valkyrie.defense(13, fire=0.9, earth=1.0, energy=1.0, ice=0.9, holy=0.95, death=1.05, physical=1.1, drown=1.0)
Valkyrie.melee(70)
Valkyrie.distance(40, ANIMATION_SPEAR, chance(21))
Valkyrie.loot( ("girlish hair decoration", 5.5), ("red apple", 11.5, 2), ("hunting spear", 4.75), ("meat", 29.75, 3), (2148, 100, 12), ("spear", 100, 3), ("chain armor", 8.0), ("protective charm", 2.75), ("plate armor", 1.25), ("skull", 0.5), ("protection amulet", 0.75), ("double axe", 0.25), ("health potion", 0.25) )