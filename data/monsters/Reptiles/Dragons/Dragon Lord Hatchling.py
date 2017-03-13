dragon_lord_hatchling = genMonster("Dragon Lord Hatchling", 8, 5980)
dragon_lord_hatchling.health(750)
dragon_lord_hatchling.type("blood")
dragon_lord_hatchling.defense(armor=30, fire=0, earth=0.75, energy=1.05, ice=1.1, holy=1, death=1, physical=1, drown=1)
dragon_lord_hatchling.experience(645)
dragon_lord_hatchling.speed(200)
dragon_lord_hatchling.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=80)
dragon_lord_hatchling.walkAround(energy=1, fire=0, poison=1)
dragon_lord_hatchling.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
dragon_lord_hatchling.voices("Fchu?", "Rooawwrr")
dragon_lord_hatchling.loot( (2148, 100, 169), ("dragon ham", 69.75), ("green mushroom", 0.5), ("mana potion", 0.5), ("magma boots", 0.0025) )

dfwave = spell.Spell("drag fwave", target=TARGET_AREA)
dfwave.area(AREA_WAVE7)
dfwave.element(FIRE)
dfwave.effects(area=EFFECT_HITBYFIRE)
 
dragon_lord_hatchling.melee(90)
dragon_lord_hatchling.targetSpell(2305, 55, 105, check=chance(20)) #firebomb
dragon_lord_hatchling.targetSpell("drag fwave", 90, 125, check=chance(20))
dragon_lord_hatchling.targetSpell(2304, 100, 200, check=chance(20)) #gfb
dragon_lord_hatchling.selfSpell("Light Healing", 25, 55, check=chance(18))
#shoot fireball too?