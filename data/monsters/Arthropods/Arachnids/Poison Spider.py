poison_spider = genMonster("Poison Spider", 36, 5974)
poison_spider.health(26)
poison_spider.type("slime")
poison_spider.defense(armor=2, fire=1.1, earth=0, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
poison_spider.experience(22)
poison_spider.speed(160)#incorrect speed
poison_spider.behavior(summonable=270, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=6)
poison_spider.walkAround(energy=1, fire=1, poison=0)
poison_spider.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
poison_spider.loot( (2148, 61.25, 4), ("poison spider shell", 1.25) )

poison_spider.melee(20, condition=CountdownCondition(CONDITION_POISON, 2), conditionChance=100)