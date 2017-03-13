bogl_frog = genMonster("Bog Frog", 226, 6079) #corpse?
bogl_frog.outfit(255, 255, 255, 255) #color
bogl_frog.targetChance(10)
bogl_frog.type("blood")
bogl_frog.health(25)
bogl_frog.experience(0)
bogl_frog.speed(200) #incorrect
bogl_frog.walkAround(1,1,1) #?
bogl_frog.behavior(summonable=0, hostile=False, illusionable=True, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=25) #pushable?
bogl_frog.voices("Ribbit!", "Ribbit! Ribbit!")
bogl_frog.immunity(0,0,0) # paralyze, invisible, lifedrain
