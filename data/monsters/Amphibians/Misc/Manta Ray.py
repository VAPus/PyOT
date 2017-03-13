manta_ray = genMonster("Manta Ray", 449, 15276)
manta_ray.health(680)
manta_ray.type("blood")
manta_ray.defense(armor=15, fire=0, earth=0, energy=1.05, ice=1, holy=1, death=1, physical=1, drown=0)
manta_ray.experience(125)
manta_ray.speed(250) #?
manta_ray.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
manta_ray.walkAround(energy=0, fire=0, poison=0)
manta_ray.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
manta_ray.voices("Flap flap flap!")

manta_ray.melee(110, condition=CountdownCondition(CONDITION_POISON, 6), conditionChance=100)