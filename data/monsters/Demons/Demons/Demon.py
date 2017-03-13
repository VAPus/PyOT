demon = genMonster("Demon", 35, 5995)
demon.health(8200)
demon.type("blood")
demon.defense(armor=48, fire=0, earth=0.6, energy=0.5, ice=1.12, holy=1.12, death=0.8, physical=0.75, drown=1)
demon.experience(6000)
demon.speed(280)
demon.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
demon.walkAround(energy=0, fire=0, poison=0)
demon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
demon.summon("Fire Elemental", 10)
demon.maxSummons(2)
demon.voices("Your soul will be mine!", "CHAMEK ATH UTHUL ARAK!", "I SMELL FEEEEAAAAAR!", "Your resistance is futile!", "MUHAHAHA")
demon.loot( (2148, 100, 200), ("platinum coin", 70.25), ("fire axe", 4.0), ("fire mushroom", 69.75, 6), ("double axe", 19.5), ("gold ring", 1.25), ("great mana potion", 30.0, 3), ("platinum amulet", 0.75), ("small emerald", 10.25), ("orb", 3.0), ("assassin star", 15.25, 5), ("talon", 3.25), ("golden sickle", 1.5), ("stealth ring", 1.5), ("ultimate health potion", 40.0, 3), ("ice rapier", 0.5), ("giant sword", 1.75), ("demon shield", 0.75), ("devil helmet", 1.25), ("ring of healing", 0.5), ("demon horn", 0.5), ("mastermind shield", 0.5), ("purple tome", 1.25), ("golden legs", 0.5), ("might ring", 0.25), ("demonrage sword", 0.0025), ("magic plate armor", 0.0025), (7393, 0.0025) )
 
dgfb = spell.Spell("demon geb")
dgfb.area(AREA_BEAM7)
dgfb.element(LIFEDRAIN)
dgfb.effects(area=EFFECT_ENERGYAREA) #wrong effect
 
des = spell.Spell("demon estrike", target=TARGET_TARGETONLY)
des.area(AREA_WAVE1)
des.range(1)
des.element(ENERGY)
des.effects(area=EFFECT_ENERGYAREA, shoot=ANIMATION_ENERGY) #wrong effect
 
dmd = spell.Spell("demon manadrain", target=TARGET_TARGETONLY)
dmd.area(AREA_WAVE1)
dmd.targetEffect(callback=spell.mana(1, 1, 0, 120))
 
demon.melee(520)
demon.targetSpell("Hells Core", 150, 250, check=chance(9)) #
demon.targetSpell("demon geb", 300, 460, check=chance(9)) #
demon.targetSpell("demon estrike", 210, 300, check=chance(9)) #
demon.targetSpell("demon manadrain", 0, 120, check=chance(9)) #
demon.selfSpell("Light Healing", 1, 250, check=chance(9)) #
demon.targetSpell(2301, 1, 1, check=chance(9)) #use rune id
##need to add haste spells
