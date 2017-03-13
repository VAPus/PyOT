ghastly_dragon = genMonster("Ghastly Dragon", 351, 11362)
ghastly_dragon.health(7800)
ghastly_dragon.type("undead")
ghastly_dragon.defense(armor=33, fire=0.9, earth=0, energy=0.9, ice=0.5, holy=1.15, death=0, physical=1.1, drown=1)
ghastly_dragon.experience(4600)
ghastly_dragon.speed(410)
ghastly_dragon.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
ghastly_dragon.walkAround(energy=1, fire=1, poison=0)
ghastly_dragon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
ghastly_dragon.voices("EMBRACE MY GIFTS!", "I WILL FEAST ON YOUR SOUL!")
ghastly_dragon.loot( ("ghastly dragon head", 6.5), ("ultimate health potion", 5.0), ("jade hat", 0.75), ("soul orb", 12.0), ("zaoan halberd", 8.0), ("great spirit potion", 3.75), ("platinum coin", 45.5, 2), ("zaoan armor", 0.75), ("great health potion", 10.25), ("undead heart", 21.0), (2148, 100, 268), ("demonic essence", 9.0, 3), ("rusty armor", 3.0), ("zaoan legs", 1.25), ("twin hooks", 5.25), ("drakinata", 0.5), ("spellweaver's robe", 0.75), ("shiny stone", 0.75), ("guardian boots", 0.25), ("zaoan sword", 0.0025), ("zaoan shoes", 1.0), ("zaoan helmet", 0.25) )

#poisons (starting up from 46-63 hp per turn), Cursing Death Hit (40-500) (+20% each turn, 5-7 turns), Paralyze --little bat effects.
gdwwave = spell.Spell("ghastly wwave", target=TARGET_AREA)
gdwwave.area(AREA_WAVE5)
gdwwave.element(FIRE) #?
gdwwave.effects(area=EFFECT_WATERSPLASH)

ghdball = spell.Spell("ghastly dball")
ghdball.area(AREA_CIRCLE3)
ghdball.element(DEATH)
ghdball.effects(area=EFFECT_HITAREA)

gdld = spell.Spell("ghastly lifedrain", target=TARGET_TARGETONLY)
gdld.element(PHYSICAL) #life drain
gdld.effects(area=EFFECT_MAGIC_RED)

ghastly_dragon.melee(650)
ghastly_dragon.targetSpell("ghastly wwave", 50, 250, check=chance(20))
ghastly_dragon.targetSpell("ghastly dball", 1, 180, check=chance(20))
ghastly_dragon.targetSpell("ghastly lifedrain", 80, 228, check=chance(20))