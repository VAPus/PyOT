killer_caiman = genMonster("Killer Caiman ", 358, 11138)
killer_caiman.health(1500)
killer_caiman.type("blood")
killer_caiman.defense(armor=45, fire=1, earth=0.8, energy=1.05, ice=0.9, holy=1, death=1, physical=0.95, drown=1)
killer_caiman.experience(800)
killer_caiman.speed(240) #?
killer_caiman.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
killer_caiman.walkAround(energy=1, fire=1, poison=1)
killer_caiman.immunity(paralyze=0, invisible=1, lifedrain=0, drunk=0)
killer_caiman.melee(180)
killer_caiman.selfSpell("Haste", 360, 360, length=8, check=chance(9)) #strength
killer_caiman.loot( ("piece of crocodile leather", 9.75), (2148, 100, 177), ("ham", 39.25), (7632, 0.5), ("bunch of ripe rice", 7.5, 2), ("small emerald", 1.0), ("crocodile boots", 0.0025) )