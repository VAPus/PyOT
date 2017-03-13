nightslayer = genMonster("Nightslayer", 152, 6080)
nightslayer.outfit(95, 95, 95, 95)#?
nightslayer.health(400, healthmax=400)
nightslayer.type("blood")
nightslayer.defense(armor=27, fire=1, earth=1, energy=1, ice=1.1, holy=1, death=1, physical=1, drown=1)#
nightslayer.experience(250)
nightslayer.speed(250)#
nightslayer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
nightslayer.walkAround(energy=0, fire=0, poison=0)
nightslayer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
nightslayer.melee(70)#
nightslayer.loot( ("midnight shard", 17.75) )