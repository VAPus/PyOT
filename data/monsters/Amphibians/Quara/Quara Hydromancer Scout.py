quara_hydromancer_scout = genMonster("Quara Hydromancer Scout", 47, 6066)
quara_hydromancer_scout.health(1100)
quara_hydromancer_scout.type("blood")
quara_hydromancer_scout.defense(armor=33, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=1, physical=1, drown=0)
quara_hydromancer_scout.experience(800)
quara_hydromancer_scout.speed(280)
quara_hydromancer_scout.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=30)
quara_hydromancer_scout.walkAround(energy=1, fire=0, poison=1)
quara_hydromancer_scout.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
quara_hydromancer_scout.voices("Qua hah tsh!", "Teech tsha tshul!", "Quara tsha Fach!", "Tssssha Quara!", "Blubber.", "Blup.")
quara_hydromancer_scout.loot( ("white pearl", 2.25), ("fish", 15.25, 2), ("small emerald", 1.25, 2), (2148, 100, 88), ("quara eye", 9.75), ("fish fin", 1.25, 3), ("black pearl", 1.75), ("wand of cosmic energy", 1.25), ("knight armor", 0.25), ("ring of healing", 0.5) )

#Missing - Paralyze (on target?)

qhld = spell.Spell() #life drain
qhld.element(PHYSICAL) #life drain
qhld.effects(area=EFFECT_MAGIC_GREEN) #effect?

qhldb = spell.Spell(target=TARGET_AREA) #lifedrain beam
qhldb.area(AREA_BEAM7) #7 or 4?
qhldb.element(PHYSICAL) #life drain
qhldb.effects(area=EFFECT_BUBBLES)

qhbberserk = spell.Spell() #bubbler berserk
qhbberserk.area(AREA_SQUARE)
qhbberserk.element(ICE)
qhbberserk.effects(area=EFFECT_BUBBLES)

qhib = spell.Spell(target=TARGET_AREA) #ice beam
qhib.area(AREA_BEAM7) #7 or 4?
qhib.element(ICE) #life drain
qhib.effects(area=EFFECT_MAGIC_GREEN)

quara_hydromancer_scout.melee(40, condition=CountdownCondition(CONDITION_POISON, 5), conditionChance=100)
quara_hydromancer_scout.selfSpell("Light Healing", 25, 55, check=chance(20)) #strength?
quara_hydromancer_scout.targetSpell(qhldb, 125, 250, check=chance(20))
quara_hydromancer_scout.targetSpell(qhib, 1, 210, check=chance(20))
quara_hydromancer_scout.targetSpell(qhld, 45, 170, check=chance(20))
quara_hydromancer_scout.targetSpell(qhbberserk, 130, 165, check=chance(20))