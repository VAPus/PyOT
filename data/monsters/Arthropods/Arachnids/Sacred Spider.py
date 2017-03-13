#most values are unknown
Sacred_Spider = genMonster("Sacred Spider", 219, 5995)
Sacred_Spider.health(550)
Sacred_Spider.type("slime")
Sacred_Spider.defense(armor=29, fire=1.05, earth=0, energy=0.9, ice=1.1, holy=1, death=1, physical=1, drown=1)
Sacred_Spider.experience(330)
Sacred_Spider.speed(280)
Sacred_Spider.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
Sacred_Spider.walkAround(energy=1, fire=1, poison=0)
Sacred_Spider.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
Sacred_Spider.loot( (2148, 100, 118), (8859, 27.5), ("plate armor", 5.5), ("scarab coin", 12.5, 4), ("gold ingot", 0.25) )

Sacred_Spider.melee(150, condition=CountdownCondition(CONDITION_POISON, 4), conditionChance=100)