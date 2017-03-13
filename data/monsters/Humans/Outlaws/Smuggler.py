Smuggler = genMonster("Smuggler", 134, 6080)
Smuggler.outfit(95, 0, 113, 115)
Smuggler.targetChance(10)
Smuggler.type("blood")
Smuggler.health(130)
Smuggler.experience(48)
Smuggler.speed(176) # Correct
Smuggler.walkAround(1,1,1) # energy, fire, poison
Smuggler.behavior(summonable=390, hostile=True, illusionable=True, convinceable=390, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=13)
Smuggler.voices("You saw something you shouldn't", "I will silence you forever!")
Smuggler.immunity(0,0,0) # paralyze, invisible, lifedrain
Smuggler.defense(9, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.05, drown=1.0)
Smuggler.melee(60)
Smuggler.loot( (2148, 100, 10), ("leather legs", 14.5), ("torch", 45.0, 2), ("ham", 10.0), ("combat knife", 4.0), ("knife", 10.0), ("leather helmet", 10.25), ("short sword", 10.25), ("raspberry", 16.75, 5), ("sword", 4.5), ("deer trophy", 0.25) )