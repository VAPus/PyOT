Deepling_Warrior = genMonster("Deepling Warrior", 441, 15188)
Deepling_Warrior.health(1600, healthmax=1600)
Deepling_Warrior.type("blood")
Deepling_Warrior.defense(armor=1, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=0.9, physical=1, drown=0)
Deepling_Warrior.experience(1500)
Deepling_Warrior.speed(250) ##?
Deepling_Warrior.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=30)
Deepling_Warrior.walkAround(energy=1, fire=0, poison=1)
Deepling_Warrior.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Deepling_Warrior.voices("Jou wjil ajll djie!")

Deepling_Warrior.melee(300)
Deepling_Warrior.selfSpell("Light Healing", 50, 150, check=chance(20)) #strength?
Deepling_Warrior.targetSpell("Whirlwind Throw", 1, 290, check=chance(21)) #goes by weapon, will it work?
