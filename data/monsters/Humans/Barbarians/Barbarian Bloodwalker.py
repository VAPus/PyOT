Barbarian_Bloodwalker = genMonster("Barbarian Bloodwalker", 255, 6080)
Barbarian_Bloodwalker.outfit(114,132,132,132)
Barbarian_Bloodwalker.targetChance(10)
Barbarian_Bloodwalker.type("blood")
Barbarian_Bloodwalker.health(305)
Barbarian_Bloodwalker.experience(195)
Barbarian_Bloodwalker.speed(236) # correct
Barbarian_Bloodwalker.walkAround(1,1,1) # energy, fire, poison
Barbarian_Bloodwalker.behavior(summonable=0, hostile=True, illusionable=False, convinceable=590, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Barbarian_Bloodwalker.voices("YAAAHEEE!", "SLAUGHTER!", "CARNAGE!", "You can run but you can't hide")
Barbarian_Bloodwalker.immunity(0,0,0) # paralyze, invisible, lifedrain
Barbarian_Bloodwalker.defense(9, fire=1.0, earth=1.05, energy=0.9, ice=0.5, holy=0.8, death=1.1, physical=0.9, drown=1.0)
Barbarian_Bloodwalker.melee(200)
Barbarian_Bloodwalker.loot( (2148, 100, 12), ("chain helmet", 10.75), ("chain armor", 9.75), ("battle axe", 6.25), ("ham", 7.5), ("lamp", 8.5), ("halberd", 7.0), ("shard", 0.25), ("red piece of cloth", 0.75, 3), ("health potion", 1.25), ("beastslayer axe", 0.25), ("fur boots", 0.25) )