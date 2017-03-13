midnight_warrior = genMonster("Midnight Warrior", 8, 5980)
midnight_warrior.outfit(95, 95, 95, 95)#
midnight_warrior.health(1000)
midnight_warrior.type("blood")
midnight_warrior.defense(armor=24, fire=1.1, earth=0, energy=0.8, ice=0.8, holy=1, death=1, physical=0.85, drown=1)#
midnight_warrior.experience(750)
midnight_warrior.speed(300)#
midnight_warrior.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
midnight_warrior.walkAround(energy=0, fire=0, poison=0)
midnight_warrior.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
midnight_warrior.voices("I am champion of darkness and you are nothing.")
midnight_warrior.melee(150, condition=CountdownCondition(CONDITION_POISON, 7), conditionChance=100)
midnight_warrior.loot( ("midnight shard", 7.0) )