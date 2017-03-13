#mostly unknown
doomsday_cultist = genMonster("Doomsday Cultist", 194, 6080)
doomsday_cultist.outfit(95, 95, 95, 95) #need correct colors
doomsday_cultist.health(125)
doomsday_cultist.type("blood")
doomsday_cultist.defense(armor=9, fire=1, earth=0.8, energy=0.7, ice=0.9, holy=1.2, death=0, physical=1, drown=1)
doomsday_cultist.experience(100)
doomsday_cultist.speed(250)
doomsday_cultist.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
doomsday_cultist.walkAround(energy=0, fire=0, poison=0)
doomsday_cultist.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
doomsday_cultist.melee(100)
doomsday_cultist.loot( ("midnight shard", 2.75) )