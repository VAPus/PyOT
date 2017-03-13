Crazed_Beggar = genMonster("Crazed Beggar", 153, 6080)
Crazed_Beggar.outfit(38, 97, 59, 38)
Crazed_Beggar.addons(3)
Crazed_Beggar.targetChance(0)
Crazed_Beggar.type("blood")
Crazed_Beggar.health(100)
Crazed_Beggar.experience(35)
Crazed_Beggar.speed(134) # Correct
Crazed_Beggar.walkAround(1,1,1) # energy, fire, poison
Crazed_Beggar.behavior(summonable=300, hostile=True, illusionable=False, convinceable=300, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
Crazed_Beggar.voices("Hehehe!", "Raahhh!", "You are one of THEM! Die!", "Wanna buy roses??", "Make it stop!")
Crazed_Beggar.immunity(0,0,0) # paralyze, invisible, lifedrain
Crazed_Beggar.defense(4, fire=1.0, earth=1.1, energy=0.8, ice=1.0, holy=0.9, death=1.1, physical=0.9, drown=1.0)
Crazed_Beggar.melee(25)
Crazed_Beggar.loot( ("wooden spoon", 9.25), (2148, 100, 9), ("dirty cape", 62.25), ("roll", 19.0), ("meat", 9.0, 2), ("wooden hammer", 9.75), ("rolling pin", 5.0), ("red rose", 4.75), (1681, 0.25), ("rum flask", 0.5), ("lute", 0.25), ("rusty armor", 0.5), ("sling herb", 0.25), ("very noble-looking watch", 0.25), ("dwarven ring", 0.0025) )