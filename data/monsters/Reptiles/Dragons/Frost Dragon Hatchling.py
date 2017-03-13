frost_dragon_hatchling = genMonster("Frost Dragon Hatchling", 283, 7969)
frost_dragon_hatchling.health(800)
frost_dragon_hatchling.type("undead")
frost_dragon_hatchling.defense(armor=35, fire=0, earth=0, energy=1.05, ice=0, holy=1, death=1, physical=1, drown=1)
frost_dragon_hatchling.experience(745)
frost_dragon_hatchling.speed(170)
frost_dragon_hatchling.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=100)
frost_dragon_hatchling.walkAround(energy=1, fire=0, poison=0)
frost_dragon_hatchling.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
frost_dragon_hatchling.voices("Rooawwrr", "Fchu?")
frost_dragon_hatchling.loot( ("spellbook of enlightenment", 0.5), ("frosty heart", 5.0), ("dragon ham", 80.0), (2148, 100, 55), ("health potion", 0.5) )

fdhwave = spell.Spell("fdh iwave", target=TARGET_AREA)
fdhwave.area(AREA_WAVE42)
fdhwave.element(ICE)
fdhwave.effects(area=EFFECT_ICEATTACK)

frost_dragon_hatchling.melee(160)
frost_dragon_hatchling.selfSpell("Light Healing", 40, 60, check=chance(18))
frost_dragon_hatchling.targetSpell("fdh iwave", 60, 110, check=chance(20))
frost_dragon_hatchling.targetSpell(2274, 60, 110, check=chance(20)) #avalache
#Distance Paralyze missing