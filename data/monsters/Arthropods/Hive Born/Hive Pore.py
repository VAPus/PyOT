hive_pore = genMonster("Hive Pore", 0, 5980) #is the name visable? incorrect look no corpse?
hive_pore.health(1, healthmax=1)
hive_pore.type("slime")
hive_pore.defense(armor=10, fire=0, earth=0, energy=0, ice=0, holy=0, death=0, physical=0, drown=0)
hive_pore.experience(0)
hive_pore.speed(0) #doesnt move
hive_pore.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
hive_pore.walkAround(energy=0, fire=0, poison=0)
hive_pore.immunity(paralyze=0, invisible=1, lifedrain=0, drunk=0)
hive_pore.summon("Lesser Swarmer", 25)
hive_pore.maxSummons(3)