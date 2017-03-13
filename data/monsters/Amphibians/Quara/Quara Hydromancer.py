quara_hydromancer = genMonster("Quara Hydromancer", 47, 6066)
quara_hydromancer.health(1100)
quara_hydromancer.type("blood")
quara_hydromancer.defense(armor=33, fire=0, earth=1.1, energy=1.25, ice=0, holy=1, death=1, physical=1, drown=0)
quara_hydromancer.experience(800)
quara_hydromancer.speed(520)
quara_hydromancer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=30)
quara_hydromancer.walkAround(energy=1, fire=0, poison=1)
quara_hydromancer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
quara_hydromancer.voices("Qua hah tsh!", "Teech tsha tshul!", "Quara tsha Fach!", "Tssssha Quara!", "Blubber.", "Blup.")
quara_hydromancer.loot( (2148, 100, 90), ("white pearl", 1.75), ("black pearl", 2.0), ("small emerald", 1.5, 2), ("quara eye", 10.25), ("shrimp", 5.0), ("knight armor", 0.25), ("fish fin", 1.0, 3), ("wand of cosmic energy", 1.0), ("ring of healing", 0.5), ("great mana potion", 1.0) )

#Missing - Paralyze (on target?)

qhld = spell.Spell() #lifedrain
qhld.element(PHYSICAL) #life drain
qhld.effects(area=EFFECT_MAGIC_GREEN) #effect?

qhldb = spell.Spell(target=TARGET_AREA) #lifedrain beam
qhldb.area(AREA_BEAM7) #7 or 4?
qhldb.element(PHYSICAL) #life drain
qhldb.effects(area=EFFECT_MAGIC_GREEN)

qhbberserk = spell.Spell() #bubble berserk
qhbberserk.area(AREA_SQUARE)
qhbberserk.element(ICE)
qhbberserk.effects(area=EFFECT_BUBBLES)

qhib = spell.Spell(target=TARGET_AREA) #ice beam
qhib.area(AREA_BEAM7) #7 or 4?
qhib.element(ICE) #life drain
qhib.effects(area=EFFECT_BUBBLES)

quara_hydromancer.melee(80, condition=CountdownCondition(CONDITION_POISON, 5), conditionChance=100)
quara_hydromancer.selfSpell("Light Healing", 25, 55, check=chance(20)) #strength?
quara_hydromancer.targetSpell(qhldb, 170, 240, check=chance(20))
quara_hydromancer.targetSpell(qhib, 100, 180, check=chance(20))
quara_hydromancer.targetSpell(qhld, 1, 170, check=chance(20))
quara_hydromancer.targetSpell(qhbberserk, 90, 150, check=chance(20))