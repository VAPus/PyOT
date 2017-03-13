quara_constrictor_scout = genMonster("Quara Constrictor Scout", 46, 6065)
quara_constrictor_scout.health(450)
quara_constrictor_scout.type("blood")
quara_constrictor_scout.defense(armor=15, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=1, physical=1, drown=0)
quara_constrictor_scout.experience(200)
quara_constrictor_scout.speed(290)
quara_constrictor_scout.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=20)
quara_constrictor_scout.walkAround(energy=1, fire=0, poison=1)
quara_constrictor_scout.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=1)
quara_constrictor_scout.voices("Boohaa!", "Tssss!", "Gluh! Gluh!", "Gaaahhh!")
quara_constrictor_scout.loot( ("longsword", 4.75), ("brass armor", 1.75), (2148, 100, 40), ("quara tentacle", 7.0), ("fish fin", 0.5, 3), ("small amethyst", 0.25) )

qcslifedrain_berserk = spell.Spell() #lifedrain berserk
qcslifedrain_berserk.area(AREA_SQUARE)
qcslifedrain_berserk.element(LIFEDRAIN)
qcslifedrain_berserk.effects(area=EFFECT_MAGIC_RED) #?

quara_constrictor_scout.melee(130) #or more
quara_constrictor_scout.targetSpell(qcslifedrain_berserk, 1, 80, check=chance(25))