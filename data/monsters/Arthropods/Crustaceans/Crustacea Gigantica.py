Crustacea_Gigantica = genMonster("Crustacea Gigantica", 8, 5980) ##looktype corpse
Crustacea_Gigantica.health(1600, healthmax=1600)
Crustacea_Gigantica.type("blood")
Crustacea_Gigantica.defense(armor=1, fire=1, earth=1, energy=1, ice=0, holy=1, death=1, physical=1, drown=1)
Crustacea_Gigantica.experience(1800)
Crustacea_Gigantica.speed(300) ##?
Crustacea_Gigantica.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
Crustacea_Gigantica.walkAround(energy=0, fire=0, poison=0)
Crustacea_Gigantica.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
Crustacea_Gigantica.voices("Chrchrchr", "Klonklonk", "Chrrrrr")

Crustacea_Gigantica.melee(160)