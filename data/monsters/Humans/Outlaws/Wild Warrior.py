Wild_Warrior = genMonster("Wild Warrior", 131, 6080)
Wild_Warrior.outfit(57, 57, 57, 57)
Wild_Warrior.targetChance(10)
Wild_Warrior.type("blood")
Wild_Warrior.health(135)
Wild_Warrior.experience(60)
Wild_Warrior.speed(190) # Correct
Wild_Warrior.walkAround(1,1,1) # energy, fire, poison
Wild_Warrior.behavior(summonable=420, hostile=True, illusionable=True, convinceable=420, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=13)
Wild_Warrior.voices("Gimme your money!", "An enemy!")
Wild_Warrior.immunity(0,0,0) # paralyze, invisible, lifedrain
Wild_Warrior.defense(11, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.1, drown=1.0)
Wild_Warrior.melee(70)
Wild_Warrior.loot( ("brass shield", 18.0), (2148, 100, 30), ("mace", 10.25), ("leather legs", 7.75), ("chain helmet", 5.0), ("steel shield", 1.0), ("axe", 29.5), ("egg", 15.5, 2), ("iron helmet", 0.75), ("brass armor", 2.5), ("doll", 0.5) )