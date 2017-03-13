Yeti = genMonster("Yeti", 8, 5980) ##looktype and corpse
Yeti.health(950)
Yeti.type("blood")
Yeti.defense(armor=1, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
Yeti.experience(460)
Yeti.speed(300) #incorrect
Yeti.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Yeti.walkAround(energy=0, fire=0, poison=0)
Yeti.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Yeti.voices("Yooodelaaahooohooo")
Yeti.melee(200)
Yeti.distance(80, ANIMATION_SNOWBALL, chance(21))