hive_overseer = genMonster("Hive Overseer", 458, 15354)
hive_overseer.health(7500, healthmax=7500)
hive_overseer.type("slime")
hive_overseer.defense(armor=75, fire=0.3, earth=0, energy=0.8, ice=1, holy=0.9, death=1, physical=0.4, drown=1)
hive_overseer.experience(100) # XXX: Wrong, just to fix loading
hive_overseer.speed(100) # XXX: Wrong, just to fix loading
hive_overseer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
hive_overseer.walkAround(energy=0, fire=0, poison=0)
hive_overseer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
hive_overseer.summon("Spidris Elite", 10)
hive_overseer.maxSummons(2)
hive_overseer.voices("Zopp!", "Kropp!")
hive_overseer.melee(450)