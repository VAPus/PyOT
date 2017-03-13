undead_cavebear = genMonster("Undead Cavebear", 384, 5995)#unknown corpse
undead_cavebear.health(450)
undead_cavebear.type("undead")
undead_cavebear.defense(armor=2, fire=1, earth=0, energy=1, ice=1, holy=1.01, death=0, physical=1, drown=1)
undead_cavebear.experience(600)
undead_cavebear.speed(100)#unknown speed
undead_cavebear.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
undead_cavebear.walkAround(energy=0, fire=0, poison=0)
undead_cavebear.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
undead_cavebear.voices("Grrrrrrrrrrr")
undead_cavebear.melee(150) #not accurate