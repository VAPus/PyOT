
mad_scientist = genMonster("Mad Scientist", 133, 6080)
mad_scientist.outfit(97, 0, 38, 97) #needs 1 addon
mad_scientist.health(325)
mad_scientist.type("blood")
mad_scientist.defense(armor=15, fire=0.9, earth=0.8, energy=0.8, ice=0.9, holy=0.8, death=1.05, physical=1, drown=0)
mad_scientist.experience(205)
mad_scientist.speed(220)
mad_scientist.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
mad_scientist.walkAround(energy=1, fire=1, poison=1)
mad_scientist.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
mad_scientist.voices("Die in the name of Science!", "You will regret interrupting my studies!", "Let me test this!", "I will study your corpse!")
mad_scientist.melee(35)
mad_scientist.loot( ("mana potion", 19.75), (2148, 100, 112), ("health potion", 21.5), ("powder herb", 6.5), (2162, 2.5), ("life crystal", 2.0), ("white mushroom", 15.75, 3), ("cookie", 3.5, 5), ("cream cake", 0.75), (7762, 0.5), ("mastermind potion", 0.0025) )