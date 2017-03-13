lesser_swarmer = genMonster("Lesser Swarmer", 460, 15385)
lesser_swarmer.health(230, healthmax=230)
lesser_swarmer.type("slime")
lesser_swarmer.defense(armor=25, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
lesser_swarmer.experience(0)
lesser_swarmer.speed(250) #incorrect
lesser_swarmer.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
lesser_swarmer.walkAround(energy=1, fire=1, poison=0) #?
lesser_swarmer.immunity(paralyze=1, invisible=0, lifedrain=1, drunk=1)
lesser_swarmer.melee(75, condition=CountdownCondition(CONDITION_POISON, 3), conditionChance=100)