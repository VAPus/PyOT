scorpion = genMonster("Scorpion", 43, 5988)
scorpion.health(45, healthmax=45)
scorpion.type("slime")
scorpion.defense(armor=15, fire=1.1, earth=0, energy=0.8, ice=1.1, holy=1, death=1, physical=1, drown=1)
scorpion.experience(45)
scorpion.speed(150)
scorpion.behavior(summonable=310, hostile=True, illusionable=True, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=5)
scorpion.walkAround(energy=1, fire=1, poison=0)
scorpion.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
scorpion.loot( ("scorpion tail", 4.75) )

scorpion.melee(50) #poison always up to 18~