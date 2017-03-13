swarmer_hatchling = genMonster("Swarmer Hatchling", 460, 15385)
swarmer_hatchling.health(5, healthmax=5)
swarmer_hatchling.type("slime")
swarmer_hatchling.defense(armor=25, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=4)
swarmer_hatchling.experience(0)
swarmer_hatchling.speed(250) #incorrect
swarmer_hatchling.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
swarmer_hatchling.walkAround(energy=0, fire=1, poison=0) #?
swarmer_hatchling.immunity(paralyze=1, invisible=0, lifedrain=1, drunk=1)
swarmer_hatchling.voices("Flzlzlzlzlzlzlz?")
swarmer_hatchling.melee(0)