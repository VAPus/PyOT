rift_scythe = genMonster("Rift Scythe", 300, 6070)#no corpse
rift_scythe.health(3600)
rift_scythe.type("undead")
rift_scythe.defense(armor=32, fire=1.1, earth=0.6, energy=1.1, ice=0.35, holy=1.1, death=0.2, physical=1.05, drown=1)
rift_scythe.experience(2000)
rift_scythe.speed(370)
rift_scythe.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
rift_scythe.walkAround(energy=1, fire=1, poison=1)
rift_scythe.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
rift_scythe.melee(200)#wrong