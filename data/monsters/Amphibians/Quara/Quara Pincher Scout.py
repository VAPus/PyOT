quara_pincher_scout = genMonster("Quara Pincher Scout", 77, 6063)
quara_pincher_scout.health(1800)
quara_pincher_scout.type("blood")
quara_pincher_scout.defense(armor=80, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=1, physical=1, drown=0)
quara_pincher_scout.experience(1200)
quara_pincher_scout.speed(250)
quara_pincher_scout.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
quara_pincher_scout.walkAround(energy=1, fire=0, poison=1)
quara_pincher_scout.immunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
quara_pincher_scout.voices("Clank! Clank!", "Clap!", "Crrrk! Crrrk!")
quara_pincher_scout.loot( ("plate armor", 4.75), ("halberd", 2.25), (12446, 9.25), (2148, 100, 149), ("fish fin", 0.75, 3), ("small ruby", 3.25, 2), ("life crystal", 1.0) )

#Close Range Paralyze (lasts for 1-3 seconds).
quara_pincher_scout.melee(240)