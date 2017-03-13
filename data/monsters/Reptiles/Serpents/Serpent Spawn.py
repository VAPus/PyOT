serpent_spawn = genMonster("Serpent Spawn", 220, 4323)
serpent_spawn.health(3000)
serpent_spawn.type("slime")
serpent_spawn.defense(armor=47, fire=1.1, earth=0, energy=1.1, ice=0.8, holy=1, death=1, physical=1, drown=1)
serpent_spawn.experience(3050)
serpent_spawn.speed(240)
serpent_spawn.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=275)
serpent_spawn.walkAround(energy=1, fire=1, poison=0)
serpent_spawn.immunity(paralyze=1, invisible=1, lifedrain=0, drunk=1)
serpent_spawn.voices("HISSSS", "I bring your deathhh, mortalssss", "Sssssouls for the one", "Tsssse one will risssse again")
serpent_spawn.loot( (2148, 100, 245), ("life ring", 6.0), ("energy ring", 6.0), ("small sapphire", 12.0), ("green mushroom", 17.75), ("power bolt", 5.75), ("great mana potion", 2.0), ("snake skin", 14.75), ("crown armor", 0.5), ("warrior helmet", 0.5), ("life crystal", 0.75), ("mercenary sword", 2.0), ("golden mug", 3.0), ("strange helmet", 0.75), ("snakebite rod", 1.0), ("old parchment", 0.5), ("winged tail", 1.0), ("noble axe", 0.75), ("royal helmet", 0.0025), ("spellbook of mind control", 0.0025), (3971, 0.25), ("tower shield", 0.75), ("swamplair armor", 0.0025) )

#Paralyze --same as a hydra pbomb, (Poison Hit (0-300) --i think this is a poison bomb which deals damage), changes your appearance into a worm.

ssmb = spell.Spell("ss musicbeam")
ssmb.area(AREA_BEAM7)
ssmb.element(PHYSICAL) #life drain
ssmb.effects(area=EFFECT_SOUND_RED)

sspwave = spell.Spell("ss pwave", target=TARGET_AREA)
sspwave.area(AREA_WAVE8)
sspwave.element(EARTH)
sspwave.effects(area=EFFECT_POISONAREA) 

serpent_spawn.melee(250)
serpent_spawn.selfSpell("Light Healing", 250, 400, check=chance(20))
serpent_spawn.selfSpell("Haste", 360, 360, length=8, check=chance(9)) #strength
serpent_spawn.targetSpell("ss musicbeam", 1, 500, check=chance(20))
serpent_spawn.targetSpell("ss musicbeam", 1, 500, check=chance(20))