Deepling_Guard = genMonster("Deepling Guard", 442, 15175)
Deepling_Guard.health(1900, healthmax=1900 )
Deepling_Guard.type("blood")
Deepling_Guard.defense(armor=1, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=0.9, physical=1, drown=1)
Deepling_Guard.experience(2100)
Deepling_Guard.speed(300) #unknown
Deepling_Guard.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=20)
Deepling_Guard.walkAround(energy=1, fire=0, poison=1)
Deepling_Guard.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Deepling_Guard.voices("QJELL NETA NA!!")

Deepling_Guard.melee(400)
Deepling_Guard.distance(350, ANIMATION_SPEAR, chance(21))
Deepling_Guard.selfSpell("Light Healing", 100, 200, check=chance(20)) #strength?
