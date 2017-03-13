Bonelord = genMonster("Bonelord", 17, 5992)
Bonelord.targetChance(10)
Bonelord.type("blood")
Bonelord.health(260)
Bonelord.experience(170)
Bonelord.speed(150) # correct
Bonelord.walkAround(1,1,0) # energy, fire, poison
Bonelord.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=4, runOnHealth=0)
Bonelord.voices("You've got the look!", "Let me take a look at you.", "Eye for eye!", "I've got to look!", "Here's looking at you!")
Bonelord.immunity(0,1,1) # paralyze, invisible, lifedrain
Bonelord.defense(5, fire=1.1, earth=1.0, energy=1.0, ice=0.8, holy=1.0, death=1.0, physical=1.0, drown=1.0)
Bonelord.summon("Skeleton", 10)
Bonelord.maxSummons(2)
Bonelord.melee(5)
Bonelord.loot( ("morning star", 6.75), ("longsword", 8.5), (2148, 100, 48), ("two handed sword", 4.0), ("spellbook", 4.75), ("steel shield", 3.5), ("small flask of eyedrops", 5.5), ("terra rod", 0.5), ("bonelord eye", 1.0), ("mana potion", 0.25), ("bonelord shield", 0.0025) )