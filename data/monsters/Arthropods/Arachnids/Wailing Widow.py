wailing_widow = genMonster("Wailing Widow", 347, 11310)
wailing_widow.health(850)
wailing_widow.type("slime")
wailing_widow.defense(armor=33, fire=1.1, earth=0, energy=1, ice=1, holy=0.9, death=0, physical=1, drown=1)
wailing_widow.experience(450)
wailing_widow.speed(280)
wailing_widow.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=366)#does it run?
wailing_widow.walkAround(energy=1, fire=1, poison=0)
wailing_widow.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
wailing_widow.loot( (2148, 100, 139), ("health potion", 4.25), ("mana potion", 2.0), (11328, 6.0), ("plate shield", 3.0), ("green mushroom", 1.25), ("zaoan halberd", 1.25), (11329, 0.5) )

wailing_widow.melee(120) #poisons you