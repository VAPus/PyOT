#move to misc/shapeshifter folder
son_of_verminor = genMonster("Son Of Verminor", 19, 1496)
son_of_verminor.health(8500)
son_of_verminor.type("slime")
son_of_verminor.defense(armor=53, fire=0.9, earth=0, energy=0.8, ice=1, holy=1, death=1, physical=1, drown=1)
son_of_verminor.experience(5900)
son_of_verminor.speed(120)#incorrect?
son_of_verminor.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
son_of_verminor.walkAround(energy=0, fire=1, poison=0)
son_of_verminor.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
son_of_verminor.voices("Blubb.")
son_of_verminor.melee(460)
#Creature Illusion (appears as a Rat, Larva, Scorpion or Slime)