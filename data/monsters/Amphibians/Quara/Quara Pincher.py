quara_pincher = genMonster("Quara Pincher", 77, 6063)
quara_pincher.health(1800)
quara_pincher.type("blood")
quara_pincher.defense(armor=94, fire=0, earth=1.1, energy=1.25, ice=0, holy=1, death=1, physical=1, drown=0)
quara_pincher.experience(1200)
quara_pincher.speed(540)
quara_pincher.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
quara_pincher.walkAround(energy=1, fire=0, poison=1)
quara_pincher.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
quara_pincher.voices("Clank! Clank!", "Clap!", "Crrrk! Crrrk!")
quara_pincher.loot( ("shrimp", 5.25), (2148, 100, 124), (12446, 15.0), ("great health potion", 0.75), ("small ruby", 8.0, 2), ("halberd", 4.75), ("fish fin", 1.5, 3), ("warrior helmet", 0.75), ("crown armor", 0.25), ("glacier robe", 0.25), ("giant shrimp", 0.0025) )

#Close Range Paralyze (lasts for 1-3 seconds).
quara_pincher.melee(340)