#mostly unknown
#always around not really a boss
energized_raging_mage = genMonster("Energized Raging Mage", 423, 5995) #unknown corpse
energized_raging_mage.health(4000)
energized_raging_mage.type("blood")
energized_raging_mage.defense(armor=30, fire=1, earth=1, energy=0, ice=1, holy=1, death=1, physical=1, drown=1)
energized_raging_mage.experience(0)
energized_raging_mage.speed(200)
energized_raging_mage.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=800)
energized_raging_mage.walkAround(energy=0, fire=0, poison=0)
energized_raging_mage.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
energized_raging_mage.voices("Behold the all permeating powers I draw from this gate!!", "ENERGY!!", "I FEEL, I FEEEEEL... OMNIPOTENCE!!", "MWAAAHAHAAA!! NO ONE!! NO ONE CAN DEFEAT MEEE!!!")
energized_raging_mage.summon("Golden Servant", 10)
energized_raging_mage.maxSummons(1)