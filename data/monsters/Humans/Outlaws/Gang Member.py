Gang_Member = genMonster("Gang Member", 151, 6080)
Gang_Member.outfit(114, 19, 42, 20)
Gang_Member.targetChance(0)
Gang_Member.type("blood")
Gang_Member.health(295)
Gang_Member.experience(70)
Gang_Member.speed(190) # Correct
Gang_Member.walkAround(1,1,1) # energy, fire, poison
Gang_Member.behavior(summonable=0, hostile=True, illusionable=True, convinceable=450, pushable=True, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=35)
Gang_Member.voices("This is our territory!", "Help me guys!", "I don't like the way you look!", "You're wearing the wrong colours!", "Don't mess with us!")
Gang_Member.immunity(0,0,0) # paralyze, invisible, lifedrain
Gang_Member.defense(9, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.05, physical=1.0, drown=1.0)
Gang_Member.melee(70)
Gang_Member.loot( (2148, 100, 30), ("leather legs", 15.5), ("brown bread", 4.25), ("mace", 9.5), ("club ring", 1.0), ("studded legs", 5.0) )