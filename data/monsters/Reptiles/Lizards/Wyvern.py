
wyvern = genMonster("Wyvern", 239, 6302)
wyvern.health(795)
wyvern.type("blood")
wyvern.defense(armor=20, fire=1, earth=0, energy=0.8, ice=0.9, holy=1, death=1, physical=1, drown=1)
wyvern.experience(515)
wyvern.speed(200)
wyvern.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=300)
wyvern.walkAround(energy=1, fire=1, poison=0)
wyvern.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
wyvern.voices("Shriiiek")
wyvern.melee(120) #(poisons you, starting from up to 24
wyvern.loot( ("dragon ham", 60.25, 3), (2148, 100, 63), ("wand of inferno", 0.75), ("power bolt", 3.5), ("wyvern talisman", 4.0), ("emerald bangle", 0.5), ("small sapphire", 0.5), ("strong health potion", 0.5), ("wyvern fang", 0.25) )