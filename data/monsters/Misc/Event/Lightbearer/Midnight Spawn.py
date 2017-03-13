#some incorrect information
midnight_spawn = genMonster("Midnight Spawn", 315, 9960)
midnight_spawn.health(320)
midnight_spawn.type("undead")
midnight_spawn.defense(armor=44, fire=0.7, earth=0.01, energy=1, ice=1.1, holy=1.1, death=0.01, physical=0.7, drown=1)
midnight_spawn.experience(300)
midnight_spawn.speed(230)
midnight_spawn.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
midnight_spawn.walkAround(energy=1, fire=1, poison=0)
midnight_spawn.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)#.99% immune to life drain?
midnight_spawn.melee(150)
midnight_spawn.loot( ("midnight shard", 13.5) )