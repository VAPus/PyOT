dragon = genMonster("Dragon", 34, 5973)
dragon.health(1000)
dragon.type("blood")
dragon.defense(armor=22, fire=0, earth=0.2, energy=0.8, ice=1.1, holy=1, death=1, physical=1, drown=1)
dragon.experience(700)
dragon.speed(180)
dragon.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=300)
dragon.walkAround(energy=0, fire=0, poison=0)
dragon.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
dragon.voices("GROOAAARRR", "FCHHHHH")
dragon.loot( ("steel shield", 14.75), (12413, 9.75), ("dragon ham", 65.0, 3), ("plate legs", 2.0), (2148, 100, 105), ("strong health potion", 1.0), ("longsword", 4.25), ("steel helmet", 3.25), ("crossbow", 10.0), ("burst arrow", 42.75, 10), ("dragonbone staff", 0.0025), ("green dragon scale", 1.25), ("dragon hammer", 0.5), ("green dragon leather", 1.0), ("broadsword", 2.0), ("serpent sword", 0.5), ("wand of inferno", 1.0), ("double axe", 1.0), ("small diamond", 0.5), ("dragon shield", 0.25), ("life crystal", 0.0025) )
 
#declare spell before regestering them to the creature
dfwave = spell.Spell("drag fwave", target=TARGET_AREA)
dfwave.area(AREA_WAVE8)
dfwave.element(FIRE)
dfwave.effects(area=EFFECT_HITBYFIRE)
 
dragon.melee(120)
#arguements are (self, spellName, min, max, interval=2, check=chance(10), range=7, length=None)
#im not sure if we are ever going to need length
dragon.targetSpell("drag fwave", 100, 170, check=chance(100))
dragon.selfSpell("Light Healing", 25, 55, check=chance(100))
dragon.targetSpell(2304, 60, 110, check=chance(100)) #runes go by rune id and use regTargetSpell too. range isnt needed default is 7