Nomad = genMonster("Nomad", 146, 6080)
Nomad.outfit(114, 20, 22, 2)
Nomad.addons(3)
Nomad.targetChance(10)
Nomad.type("blood")
Nomad.health(160)
Nomad.experience(60)
Nomad.speed(190) # Correct
Nomad.walkAround(1,1,1) # energy, fire, poison
Nomad.behavior(summonable=420, hostile=True, illusionable=False, convinceable=420, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=25)
Nomad.voices("I will leave your remains to the vultures!", "We are the true sons of the desert!", "We are swift as the wind of the desert!", "Your riches will be mine!")
Nomad.immunity(0,0,0) # paralyze, invisible, lifedrain
Nomad.defense(6, fire=0.8, earth=1.0, energy=1.0, ice=1.1, holy=0.8, death=1.1, physical=1.1, drown=1.0)
Nomad.melee(80)
Nomad.loot( (2148, 100, 39), ("axe", 18.75), ("leather legs", 8.75), ("brass shield", 10.25), ("mace", 7.5), ("brass armor", 2.25), ("chain helmet", 2.75), ("steel shield", 0.75), (8838, 8.25, 3), ("iron helmet", 0.75), ("parchment", 0.25), ("rope belt", 2.75), (12412, 1.0) )