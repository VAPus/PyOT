yielothax = genMonster("Yielothax", 408, 13752)
yielothax.health(1500)
yielothax.type("blood")
yielothax.defense(armor=20, fire=0.75, earth=0, energy=1.05, ice=1.05, holy=1, death=0.5, physical=1.1, drown=1)#
yielothax.experience(1250)
yielothax.speed(300)#
yielothax.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
yielothax.walkAround(energy=1, fire=0, poison=0)
yielothax.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
yielothax.voices("IIEEH!! Iiih iih ih iiih!!!", "Bsssssssm Bssssssm Bsssssssssssm!")
yielothax.loot( ("brown mushroom", 20.75, 3), ("strong mana potion", 19.25), (2148, 100, 221), ("wand of cosmic energy", 0.5), ("shockwave amulet", 0.5), ("might ring", 4.0), ("lightning pendant", 0.75), ("broken ring of ending", 0.25), ("small diamond", 15.5, 5), ("epee", 0.5), ("talon", 1.0), ("strong health potion", 20.0), ("yielowax", 0.25), ("mastermind potion", 0.5), ("lightning legs", 0.75), ("yielocks", 0.25) )

yielothax.melee(200)