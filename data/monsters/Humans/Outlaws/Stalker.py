Stalker = genMonster("Stalker", 128, 6080)
Stalker.outfit(95, 116, 95, 114)
Stalker.targetChance(10)
Stalker.type("blood")
Stalker.health(120)
Stalker.experience(90)
Stalker.speed(260) # Correct
Stalker.walkAround(1,1,1) # energy, fire, poison
Stalker.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Stalker.immunity(0,1,1) # paralyze, invisible, lifedrain
Stalker.defense(0, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Stalker.melee(70)
Stalker.loot( ("obsidian lance", 1.25), ("katana", 0.75), ("miraculum", 2.0), ("brass shield", 5.5), ("blank rune", 8.75), ("throwing knife", 15.5, 2), (2148, 60.75, 8), ("brass legs", 2.75) )