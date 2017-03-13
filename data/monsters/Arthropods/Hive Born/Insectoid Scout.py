#mostly unknown
insectoid_scout = genMonster("Insectoid Scout", 403, 5980)
insectoid_scout.health(230)
insectoid_scout.type("slime")
insectoid_scout.defense(armor=18, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
insectoid_scout.experience(150)
insectoid_scout.speed(250)
insectoid_scout.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
insectoid_scout.walkAround(energy=0, fire=0, poison=0)
insectoid_scout.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
insectoid_scout.voices("Klk! Klk!", "Chrrr! Chrrr!")#wrong?
insectoid_scout.melee(63, condition=CountdownCondition(CONDITION_POISON, 3), conditionChance=100)