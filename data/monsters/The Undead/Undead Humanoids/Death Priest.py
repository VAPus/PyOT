death_priest = genMonster("Death Priest", 99, 6028)#unknown corpse might be ash
death_priest.health(800)
death_priest.type("undead")
death_priest.defense(armor=42, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
death_priest.experience(750)
death_priest.speed(320)
death_priest.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
death_priest.walkAround(energy=0, fire=1, poison=0)
death_priest.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
death_priest.melee(200)#unknown?
death_priest.loot( (2148, 100, 143), ("white pearl", 3.25), ("health potion", 13.5), ("hieroglyph banner", 24.0), ("scarab coin", 22.0, 3), ("orichalcum pearl", 11.5, 4), ("mana potion", 16.0), ("spellbook", 3.25), ("ring of healing", 1.5) )