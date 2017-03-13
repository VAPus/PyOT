#still somewhat unknown
furious_orc_berserker = genMonster("Durious Orc Berserker", 35, 5995)
furious_orc_berserker.health(2, healthmax=2)
furious_orc_berserker.type("blood")
furious_orc_berserker.defense(-1)
furious_orc_berserker.experience(0)
furious_orc_berserker.speed(200)
furious_orc_berserker.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
furious_orc_berserker.walkAround(energy=0, fire=0, poison=0)
furious_orc_berserker.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
furious_orc_berserker.melee(0) #attacks but doesnt do damage?