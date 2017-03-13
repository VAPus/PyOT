grave_guard = genMonster("Grave Guard", 234, 6328)#incorrect corpse?
grave_guard.health(720)
grave_guard.type("blood")
grave_guard.defense(armor=37, fire=0, earth=1, energy=1, ice=1.1, holy=1.1, death=1, physical=1, drown=1)
grave_guard.experience(485)
grave_guard.speed(250)#unknown speed
grave_guard.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
grave_guard.walkAround(energy=0, fire=0, poison=0)
grave_guard.immunity(paralyze=0, invisible=1, lifedrain=0, drunk=1)
grave_guard.melee(200)#unknown?
grave_guard.loot( (2148, 100, 130), ("health potion", 20.25), ("grave flower", 71.25), ("daramanian waraxe", 1.0), ("mana potion", 21.75), ("scarab coin", 5.75), ("death ring", 2.0) )