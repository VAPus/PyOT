
young_sea_serpent = genMonster("Young Sea Serpent", 317, 8307)
young_sea_serpent.health(1050)
young_sea_serpent.type("blood")
young_sea_serpent.defense(armor=22, fire=0.7, earth=0, energy=1.1, ice=0, holy=1, death=1.15, physical=1.2, drown=0)
young_sea_serpent.experience(1000)
young_sea_serpent.speed(350)
young_sea_serpent.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=300)
young_sea_serpent.walkAround(energy=0, fire=0, poison=0)
young_sea_serpent.immunity(paralyze=1, invisible=0, lifedrain=1, drunk=1)
young_sea_serpent.voices("HISSSS", "CHHHRRRR")
young_sea_serpent.melee(200) #or more
young_sea_serpent.loot( ("battle hammer", 5.25), ("strong health potion", 5.0), ("strong mana potion", 4.0), ("sea serpent scale", 5.0), ("morning star", 39.75), ("battle axe", 8.0), ("rusty armor", 8.0, 2), (2148, 100, 174), ("stealth ring", 1.0), ("life crystal", 0.25), ("small sapphire", 3.0, 2) )