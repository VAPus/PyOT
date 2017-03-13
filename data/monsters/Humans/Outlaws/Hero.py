Hero = genMonster("Hero", 73, 6080)
Hero.targetChance(10)
Hero.type("blood")
Hero.health(1400)
Hero.experience(1200)
Hero.speed(280) # Correct
Hero.walkAround(0,1,0) # energy, fire, poison
Hero.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Hero.voices("Let's have a fight!", "I will sing a tune at your grave.", "Have you seen princess Lumelia?", "Welcome to my battleground!")
Hero.immunity(1,1,1) # paralyze, invisible, lifedrain
Hero.defense(39, fire=0.7, earth=0.5, energy=0.6, ice=0.9, holy=0.5, death=1.2, physical=0.9, drown=1.0)
Hero.melee(240)
Hero.distance(120, ANIMATION_ARROW, chance(21))
Hero.loot( ("green tunic", 8.25), ("scroll of heroic deeds", 5.5), ("meat", 9.75), ("scroll", 44.75), (2148, 100, 100), ("arrow", 100, 13), ("red rose", 19.75), ("sniper arrow", 29.25, 4), ("grapes", 20.0), ("bow", 13.25), ("lyre", 1.5), ("red piece of cloth", 2.25, 3), ("wedding ring", 5.25), ("rope", 2.5), ("crown armor", 0.5), ("great health potion", 0.5), ("two handed sword", 1.25), ("scarf", 0.75), ("war hammer", 1.25), ("small notebook", 1.0), ("might ring", 1.0), ("piggy bank", 0.25), ("crown helmet", 0.5), ("crown legs", 0.5), ("crown shield", 0.25), ("fire sword", 0.5) )