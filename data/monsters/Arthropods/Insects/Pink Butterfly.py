butterfly = genMonster("Butterfly", 213, 4993)
butterfly.health(2)
butterfly.type("slime")
butterfly.defense(armor=2, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1)
butterfly.speed(300)
butterfly.behavior(summonable=0, hostile=False, illusionable=True, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
butterfly.walkAround(energy=1, fire=1, poison=1)
#note 4313 is an old used butterfly corpse sprite or second stage of decay?