
fury = genMonster("Fury", 149, 6081)
fury.outfit(94, 77, 96, 0) #needs addons
fury.health(4100, healthmax=4100)
fury.type("blood")
fury.defense(armor=37, fire=0, earth=1.1, energy=1.1, ice=0.7, holy=0.7, death=1.1, physical=1.1, drown=1)
fury.experience(4000)
fury.speed(460)
fury.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
fury.walkAround(energy=0, fire=0, poison=0)
fury.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
fury.voices("Ahhhhrrrr!", "Waaaaah!", "Carnage!", "Dieee!")
fury.melee(509)
fury.loot( ("soul orb", 19.75), (2148, 100, 266), ("concentrated demonic blood", 68.0, 3), ("terra rod", 18.25), ("red piece of cloth", 4.25), ("platinum coin", 7.0, 4), ("demonic essence", 22.5, 3), ("great health potion", 10.75), (8844, 65.5, 4), ("small amethyst", 17.0, 3), ("assassin dagger", 0.75), ("rusty legs", 10.75), ("noble axe", 2.0), ("steel boots", 0.75), ("orichalcum pearl", 3.5, 4), ("death ring", 0.25), ("crystal ring", 0.25), ("assassin star", 0.25), ("golden legs", 0.0025) )