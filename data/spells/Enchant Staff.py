conjure = spell.Spell("Enchant Staff", "exeta vis", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=80, level=41, maglevel=0, soul=0, learned=0, vocations=(5,))
conjure.use(2401)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2433, 1))
#requires a spear