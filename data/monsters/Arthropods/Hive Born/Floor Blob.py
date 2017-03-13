floor_blob = genMonster("Floor Blob", 459, 5980)
floor_blob.health(1, healthmax=1)
floor_blob.type("slime")
floor_blob.defense(armor=10, fire=0, earth=0, energy=0, ice=0, holy=0, death=0, physical=0, drown=0)
floor_blob.experience(0)
floor_blob.speed(200) #incorrect
floor_blob.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
floor_blob.walkAround(energy=0, fire=0, poison=0)
floor_blob.immunity(paralyze=0, invisible=1, lifedrain=0, drunk=0)