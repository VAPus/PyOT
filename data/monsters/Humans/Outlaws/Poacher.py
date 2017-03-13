Poacher = genMonster("Poacher", 129, 6080)
Poacher.outfit(115, 119, 119, 115)
Poacher.addons(1)
Poacher.targetChance(10)
Poacher.type("blood")
Poacher.health(90)
Poacher.experience(70)
Poacher.speed(198) # Correct
Poacher.walkAround(1,1,1) # energy, fire, poison
Poacher.behavior(summonable=0, hostile=True, illusionable=True, convinceable=530, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=9)
Poacher.voices("You will not live to tell anyone!", "You are my game today!", "Look what has stepped into my trap!")
Poacher.immunity(0,0,0) # paralyze, invisible, lifedrain
Poacher.defense(11, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Poacher.melee(35)
Poacher.distance(35, ANIMATION_ARROW, chance(21))
Poacher.loot( ("bow", 14.75), ("leather legs", 25.75), ("leather helmet", 30.0), ("arrow", 100, 17), ("poison arrow", 4.0, 3), ("roll", 12.25, 2), ("torch", 3.5), ("closed trap", 1.0) )
