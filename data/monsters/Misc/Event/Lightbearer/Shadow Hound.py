#largely unknown
shadow_hound = genMonster("Shadow Hound", 322, 9923)
shadow_hound.health(555)
shadow_hound.type("blood")
shadow_hound.defense(armor=44, fire=1.1, earth=0, energy=1.0, ice=1.0, holy=1.25, death=0, physical=1.0, drown=1)
shadow_hound.experience(600)
shadow_hound.speed(300)
shadow_hound.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
shadow_hound.walkAround(energy=0, fire=0, poison=0)
shadow_hound.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
shadow_hound.voices("Grrrr!")
shadow_hound.melee(145)
shadow_hound.loot( ("midnight shard", 6.25) )
