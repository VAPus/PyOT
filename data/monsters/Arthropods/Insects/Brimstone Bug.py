brimstone_bug = genMonster("Brimstone Bug", 352, 12527)
brimstone_bug.type("slime")
brimstone_bug.health(1300)
brimstone_bug.experience(900)
brimstone_bug.targetChance(10)
brimstone_bug.speed(200) #incorrect
brimstone_bug.walkAround(0,1,0) # energy, fire, poison
brimstone_bug.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
brimstone_bug.voices("Chrrr!")
brimstone_bug.immunity(0,0,0) # paralyze, invisible, lifedrain
brimstone_bug.defense(38, fire=1.1, earth=0, energy=1.1, ice=1.1, holy=1.1, death=0, physical=1.05, drown=1.0)
brimstone_bug.loot( ("stealth ring", 1.0), ("strong health potion", 9.0), ("sulphurous stone", 14.75), (12658, 6.25), ("strong mana potion", 8.75), ("brimstone shell", 9.75), ("magic sulphur", 1.75), ("lump of earth", 19.75), ("small emerald", 6.0, 4), ("poisonous slime", 50.75), (2148, 100, 197), ("platinum amulet", 0.25) )
brimstone_bug.melee(150) # also poisons


#brimstone_bug.targetSpell("Wrath of Nature", 180, 270)