# bad
Slug = genMonster("Slug", 407, 6079) # not right yet
Slug.targetChance(10)
Slug.type("blood")
Slug.health(255)
Slug.experience(70)
Slug.speed(200) #incorrect
Slug.walkAround(1,1,1) # energy, fire, poison
Slug.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Slug.immunity(0,0,0) # paralyze, invisible, lifedrain
Slug.defense(9, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Slug.loot( ('gold coin', 62.5, 40), ('worm', 5, 3) )
Slug.melee(45)