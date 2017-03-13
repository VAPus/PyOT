tomb_servant = genMonster("Tomb Servant", 100, 5995)#turns into ash
tomb_servant.health(475)
tomb_servant.type("blood")
tomb_servant.defense(armor=24, fire=1.1, earth=1, energy=1, ice=1, holy=1.25, death=0, physical=1, drown=1)
tomb_servant.experience(215)
tomb_servant.speed(195)
tomb_servant.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
tomb_servant.walkAround(energy=0, fire=0, poison=0)
tomb_servant.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
tomb_servant.voices("Chaarr!!", "Ngl..Nglll...Gll")
tomb_servant.melee(130)#close~
tomb_servant.loot( (2148, 100, 107), ("longsword", 7.0), ("bone", 54.25), (3976, 100, 12), ("rotten meat", 2.0), ("bone shield", 6.0), ("scarab coin", 7.0), ("fist on a stick", 0.25), ("half-digested piece of meat", 0.5) )