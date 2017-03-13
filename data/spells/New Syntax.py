### Custom spell ###
mySpell = spell.Spell("Phoenix", "pho", icon=30, target=TARGET_AREA)
mySpell.area(AREA_CIRCLE2)
# Effects. caster, target, area and shoot
mySpell.effects(caster=EFFECT_YALAHARIGHOST, area=EFFECT_FIREAREA)

# Require, can be any field inside player.data. Mana is special since it's used!
# We also have requireLess and requireCallback if you need some complex chceks :)
mySpell.require(level=10, mana=50, maglevel=15)

# You can register as many effects as you like.
mySpell.targetEffect(health=-100) # Static effect :p
mySpell.targetEffect(callback=spell.damage(3.184, 5.59, 20, 35)) # Formula generator :)

# You can also raise conditions.
mySpell.casterCondition(Condition(CONDITION_FIRE, '', 40, damage=5)) # Side effect.
mySpell.targetCondition(Condition(CONDITION_FIRE, '', 20, damage=15)) # Side effect on target



### Conjure ###
healing = spell.Spell("Intense Healing Rune", "adura gran", icon=1, target=TARGET_SELF, group=SUPPORT_GROUP)
healing.use() # Default values are ok, ID: 2260, use=1
healing.require(mana=120, level=15, soul=1) # Require level 15, use 120mana and 1 soul point
healing.casterEffect(callback=spell.conjure(2265, 2)) # Conjure two such runes.



### Rune ###
# Rune binds to use instead of talkaction, and it default a use call.
rune = spell.Rune(2265, icon=3, count=1, group=HEALING_GROUP)
rune.require(mana=120, level=15)
rune.effects(target=EFFECT_MAGIC_BLUE)
rune.targetEffect(callback=spell.heal(3.184, 5.59, 20, 35))

# TODO:
# spell.makeField port.