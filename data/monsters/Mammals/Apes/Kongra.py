Kongra = genMonster("Kongra", 116, 6043)
Kongra.targetChance(10)
Kongra.type("blood")
Kongra.health(340)
Kongra.experience(115)
Kongra.speed(184) # Correct
Kongra.walkAround(1,1,1) # energy, fire, poison
Kongra.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=10)
Kongra.voices("Ungh! Ungh!", "Hugah!", "Huaauaauaauaa!")
Kongra.immunity(0,0,0) # paralyze, invisible, lifedrain
Kongra.defense(20, fire=0.8, earth=0.9, energy=0.95, ice=1.15, holy=1.0, death=1.05, physical=1.0, drown=1.0)
Kongra.melee(60)
Kongra.loot( ("protection amulet", 0.75), (2148, 100, 40), ("banana", 51.75, 12), ("plate armor", 1.0), ("ape fur", 1.0, 3), (12427, 5.25), ("health potion", 0.5), ("power ring", 0.25), ("club ring", 0.25) )